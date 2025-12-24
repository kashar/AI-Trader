from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import logging

import pandas as pd
import efinance as ef


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AStockIntradayDataFetcher:
    """A-shares Intraday Data Fetcher
    
    Used to batch fetch intraday K-line data for A-shares market, supports custom time period and date range.
    Supports incremental updates, automatically detects existing data and starts fetching from the day after the last date.
    
    Attributes:
        frequency: K-line frequency (minutes), default 60 minutes
        data_dir: Data storage directory
        stock_list_file: Stock list filename
        output_file: Output filename
    """
    
    def __init__(
        self,
        frequency: int = 60,
        data_dir: Optional[Path] = None,
        stock_list_file: str = "sse_50_weight.csv",
        output_file: str = "A_stock_hourly.csv"
    ) -> None:
        """Initialize data fetcher
        
        Args:
            frequency: K-line cycle (minutes), default 60 minutes
            data_dir: Data directory path, default is A_stock_data subdirectory
            stock_list_file: Stock list CSV filename (relative to script directory), default sse_50_weight.csv
            output_file: Output filename
        """
        self.frequency = frequency
        
        # 设置数据目录：默认为 A_stock_data 子目录
        if data_dir is None:
            script_dir = Path(__file__).parent
            self.data_dir = script_dir / "A_stock_data"
        else:
            self.data_dir = Path(data_dir)
        
        # 创建数据目录（如果不存在）
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 股票列表文件在 A_stock_data 目录
        self.stock_list_file = stock_list_file
        self.stock_list_path = Path(__file__).parent / "A_stock_data" / stock_list_file
        
        # 输出文件在数据目录
        self.output_file = output_file
        self.output_path = self.data_dir / output_file
        
        logger.info(f"Initialize data fetcher: frequency={frequency}mins, data_dir={self.data_dir}")
    
    def load_stock_list(self) -> List[str]:
        """Load stock code list from CSV file
        
        Read con_code column from sse_50_weight.csv, extract SSE 50 component stock codes.
        
        Returns:
            Stock code list (without suffix, e.g. '600519')
            
        Raises:
            FileNotFoundError: When stock list file does not exist
        """
        if not self.stock_list_path.exists():
            raise FileNotFoundError(f"Stock list file does not exist: {self.stock_list_path}")
        
        logger.info(f"Load stock list from {self.stock_list_path}")
        df = pd.read_csv(self.stock_list_path)
        
        # Extract unique stock codes from con_code column
        if "con_code" not in df.columns:
            raise ValueError(f"Missing 'con_code' column in file {self.stock_list_path}")
        
        stock_list = df["con_code"].unique()
        
        # Remove .SH or .SZ suffix
        stock_list = [code.replace(".SH", "").replace(".SZ", "") for code in stock_list]
        
        logger.info(f"Successfully loaded {len(stock_list)} stocks")
        logger.debug(f"Stock list: {stock_list[:5]}..." if len(stock_list) > 5 else f"Stock list: {stock_list}")
        
        return stock_list
    
    def get_date_range(self, default_start_date: str = "20251001") -> Tuple[str, str]:
        """Get data date range
        
        If output file exists, start from the day after the last day in file;
        Otherwise use default start date. End date is always today.
        
        Args:
            default_start_date: Default start date, format 'YYYYMMDD'
            
        Returns:
            Tuple[str, str]: (begin_date, end_date) format 'YYYYMMDD'
        """
        # End date is always today
        end_date = datetime.now().strftime("%Y%m%d")
        
        # Check if output file exists
        if self.output_path.exists():
            try:
                logger.info(f"Detected existing data file: {self.output_path}")
                df_existing = pd.read_csv(self.output_path)
                
                if not df_existing.empty and 'trade_date' in df_existing.columns:
                    # Get last record date
                    # trade_date format: "2025-10-09 10:30"
                    last_date_str = df_existing['trade_date'].max()
                    
                    # Extract date part (remove time)
                    last_date = datetime.strptime(last_date_str.split()[0], "%Y-%m-%d")
                    
                    # Calculate next day
                    next_date = last_date + timedelta(days=1)
                    begin_date = next_date.strftime("%Y%m%d")
                    
                    logger.info(f"Last date of existing data: {last_date.strftime('%Y-%m-%d')}")
                    logger.info(f"Will start incremental update from {begin_date}")
                    
                    # Check if already latest
                    if begin_date > end_date:
                        logger.info("Data is already up to date, no update needed")
                        return begin_date, end_date
                    
                    return begin_date, end_date
                else:
                    logger.warning("Existing file is empty or missing trade_date column, using default start date")
                    return default_start_date, end_date
                    
            except Exception as e:
                logger.warning(f"Failed to read existing data file: {e}, using default start date")
                return default_start_date, end_date
        else:
            logger.info(f"Existing data file not detected, fetching from {default_start_date}")
            return default_start_date, end_date
    
    def fetch_intraday_data(
        self,
        stock_list: List[str],
        begin_date: str,
        end_date: str
    ) -> dict:
        """Batch fetch intraday data for stocks
        
        Args:
            stock_list: List of stock codes
            begin_date: Start date, format 'YYYYMMDD'
            end_date: End date, format 'YYYYMMDD' (usually today)
            
        Returns:
            Dictionary containing data for all stocks, key is stock code, value is DataFrame
        """
        logger.info(f"Start fetching intraday data for {len(stock_list)} stocks")
        logger.info(f"Time range: {begin_date} - {end_date}, Period: {self.frequency} mins")
        
        try:
            df_dict = ef.stock.get_quote_history(
                stock_list,
                klt=self.frequency,
                beg=begin_date,
                end=end_date
            )
            logger.info("Data fetched successfully")
            return df_dict
        except Exception as e:
            logger.error(f"Data fetch failed: {e}")
            raise
    
    def process_and_save_data(
        self,
        df_dict: dict,
        is_incremental: bool = False
    ) -> pd.DataFrame:

        logger.info("Start processing data")
        
        df_new = pd.DataFrame()
        
        # Iterate over each stock's data
        for stock_code, df_one in df_dict.items():
            df_new = pd.concat([df_new, df_one], ignore_index=True)
        
        # Reset index
        df_new.reset_index(drop=True, inplace=True)
        
        # Select and rename columns
        df_new = df_new[['股票名称', '股票代码', '日期', '开盘', '收盘', '最高', '最低', '成交量']]
        df_new.columns = ['stock_name', 'stock_code', 'trade_date', 'open', 'close', 'high', 'low', 'volume']
        
        # Unify stock code format (add .SH suffix)
        df_new["stock_code"] = df_new["stock_code"].apply(lambda x: x + ".SH")
        
        # If incremental update and existing file exists, merge data
        if is_incremental and self.output_path.exists():
            try:
                logger.info("Incremental update mode: merging old and new data")
                df_old = pd.read_csv(self.output_path)
                
                # Merge old and new data
                df_total = pd.concat([df_old, df_new], ignore_index=True)
                
                # Deduplicate (data based on stock_code and trade_date, keep last)
                df_total = df_total.drop_duplicates(
                    subset=['stock_code', 'trade_date'],
                    keep='last'
                ).reset_index(drop=True)
                
                # Sort by date and stock code
                df_total = df_total.sort_values(
                    by=['trade_date', 'stock_code']
                ).reset_index(drop=True)
                
                logger.info(f"Total records after merge: {len(df_total)} (Old: {len(df_old)}, New: {len(df_new)})")
            except Exception as e:
                logger.warning(f"Failed to merge data: {e}, will only save new data")
                df_total = df_new
        else:
            df_total = df_new
        
        # Save to CSV
        df_total.to_csv(self.output_path, index=False, encoding='utf-8')
        logger.info(f"Data saved to: {self.output_path}")
        logger.info(f"Total {len(df_total)} records")
        
        return df_total
    
    def run(
        self,
        default_start_date: str = "20251001",
        auto_date_range: bool = True
    ) -> Optional[pd.DataFrame]:

        try:
            # 1. Load stock list
            stock_list = self.load_stock_list()
            
            # 2. Determine date range
            if auto_date_range:
                begin_date, end_date = self.get_date_range(default_start_date)
                
                # Check if update needed
                if begin_date > end_date:
                    logger.info("Data is up to date, no update needed")
                    # Return existing data
                    if self.output_path.exists():
                        return pd.read_csv(self.output_path)
                    return None
                    
                is_incremental = self.output_path.exists()
            else:
                begin_date = default_start_date
                end_date = datetime.now().strftime("%Y%m%d")
                is_incremental = False
            
            # 3. Fetch intraday data
            logger.info(f"Data fetch date range: {begin_date} - {end_date}")
            df_dict = self.fetch_intraday_data(stock_list, begin_date, end_date)
            
            # 4. Process and save data
            df_total = self.process_and_save_data(df_dict, is_incremental)
            
            logger.info("Data fetch process completed")
            return df_total
            
        except Exception as e:
            logger.error(f"Data fetch process failed: {e}")
            raise


def main():
    # Create data fetcher instance
    fetcher = AStockIntradayDataFetcher(
        frequency=60,  # 60 mins K-line
        stock_list_file="sse_50_weight.csv",  # SSE 50 weights file
        output_file="A_stock_hourly.csv"
    )
    
    # Execute data fetch (auto date range detection)
    df = fetcher.run(
        default_start_date="20251001",  # Only used for first run
        auto_date_range=True  # Enable auto date range detection
    )
    
    # Show data overview
    if df is not None and not df.empty:
        print("\n" + "="*50)
        print("Data Overview:")
        print("="*50)
        print(df.head(10))
        print(f"\nData Shape: {df.shape}")
        print(f"Stock Count: {df['stock_code'].nunique()}")
        print(f"Date Range: {df['trade_date'].min()} - {df['trade_date'].max()}")
    else:
        print("\n" + "="*50)
        print("No new data or data fetch failed")
        print("="*50)


if __name__ == "__main__":
    main()

