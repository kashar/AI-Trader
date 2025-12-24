# Free AI Provider Setup Guide

This guide shows you how to get free API keys for running the forex trading agent without cost.

## 🌟 Recommended: Google Gemini (Currently Enabled)

**Best for:** Free tier with generous limits, fast responses

### Setup Steps:
1. Go to https://aistudio.google.com/app/apikey
2. Click "Get API Key" or "Create API Key"
3. Copy your API key
4. Add to `.env` file:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```

**Free Tier Limits:**
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per day
- **Cost:** FREE forever

### Test It:
```bash
# Run forex agent with Gemini
python main.py configs/default_forex_config.json
```

---

## 🚀 Alternative Free Providers

### 1. Groq (Fast Inference)

**Models:** Llama 3.3 70B, Llama 3.1 70B, Mixtral 8x7B

**Setup:**
1. Go to https://console.groq.com
2. Sign up with Google/GitHub
3. Navigate to API Keys section
4. Create new API key
5. Add to `.env`:
   ```bash
   GROQ_API_KEY=your_api_key_here
   ```

**Free Tier:**
- 30 requests per minute
- 14,400 requests per day
- **Cost:** FREE

**Enable in config:**
```json
{
  "name": "llama-3.3-70b-versatile",
  "enabled": true
}
```

---

### 2. DeepSeek (Powerful & Cheap)

**Models:** DeepSeek Chat (V3)

**Setup:**
1. Go to https://platform.deepseek.com
2. Sign up and verify email
3. Go to API Keys
4. Create new key
5. Add to `.env`:
   ```bash
   DEEPSEEK_API_KEY=your_api_key_here
   ```

**Free Tier:**
- $5 free credits for new users
- Very affordable rates after free tier
- **Cost:** $0.14 per million tokens (extremely cheap)

**Enable in config:**
```json
{
  "name": "deepseek-chat",
  "enabled": true
}
```

---

### 3. Alibaba Qwen (Chinese Provider)

**Models:** Qwen Turbo

**Setup:**
1. Go to https://dashscope.aliyun.com
2. Create Alibaba Cloud account
3. Get DashScope API key
4. Add to `.env`:
   ```bash
   DASHSCOPE_API_KEY=your_api_key_here
   ```

**Free Tier:**
- 1 million tokens free per month
- **Cost:** FREE for first month

**Enable in config:**
```json
{
  "name": "qwen-turbo",
  "enabled": true
}
```

---

## 📋 Complete .env Configuration

Add these lines to your `.env` file (only add keys you've obtained):

```bash
# Google Gemini (Recommended - FREE forever)
GOOGLE_API_KEY=your_google_api_key_here

# Groq (Fast, FREE)
GROQ_API_KEY=your_groq_api_key_here

# DeepSeek (Very cheap, $5 free credits)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Alibaba Qwen (FREE tier)
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# OpenAI (if you have credits)
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🎯 Quick Start with Free Provider

### Option 1: Google Gemini (Recommended)

1. **Get API Key:** https://aistudio.google.com/app/apikey
2. **Add to .env:**
   ```bash
   GOOGLE_API_KEY=your_key_here
   ```
3. **Run:**
   ```bash
   python main.py configs/default_forex_config.json
   ```

### Option 2: Groq (Fastest)

1. **Get API Key:** https://console.groq.com
2. **Add to .env:**
   ```bash
   GROQ_API_KEY=your_key_here
   ```
3. **Edit config** to enable Groq:
   ```json
   {
     "name": "llama-3.3-70b-versatile",
     "enabled": true
   }
   ```
   And disable Gemini:
   ```json
   {
     "name": "gemini-2.0-flash-exp",
     "enabled": false
   }
   ```
4. **Run:**
   ```bash
   python main.py configs/default_forex_config.json
   ```

---

## 🔄 Switching Between Providers

Edit `configs/default_forex_config.json`:

1. Set `"enabled": false` for current provider
2. Set `"enabled": true` for new provider
3. Run the agent

Example:
```json
{
  "models": [
    {
      "name": "gemini-2.0-flash-exp",
      "enabled": false  // Disable this
    },
    {
      "name": "llama-3.3-70b-versatile",
      "enabled": true   // Enable this
    }
  ]
}
```

---

## 📊 Provider Comparison

| Provider | Free Tier | Speed | Quality | Best For |
|----------|-----------|-------|---------|----------|
| **Google Gemini** | ✅ Unlimited FREE | Fast | Excellent | General use |
| **Groq** | ✅ 14,400/day | ⚡ Fastest | Very Good | Speed critical |
| **DeepSeek** | $5 credits | Fast | Excellent | Cost efficiency |
| **Qwen** | 1M tokens/mo | Medium | Good | Chinese markets |

---

## ⚠️ Common Issues

### "Connection error"
- Check your internet connection
- Verify API key is correct in `.env`
- Ensure no typos in API endpoint URLs

### "Invalid API key"
- Regenerate API key from provider dashboard
- Check `.env` file has correct variable name
- Restart terminal after updating `.env`

### "Rate limit exceeded"
- Switch to different provider
- Wait for rate limit to reset
- Upgrade to paid tier if needed

---

## 💡 Tips for Best Results

1. **Start with Gemini** - Best free tier with no daily cost
2. **Use Groq for speed** - Fastest inference times
3. **DeepSeek for production** - Best quality/cost ratio after free credits
4. **Multiple keys** - Set up all providers to switch if one has issues

---

## 🆘 Support

If you encounter issues:
1. Check provider's status page
2. Verify API key is active in provider dashboard
3. Test with simple curl request first
4. Check `.env` file format (no quotes around values)

---

**Ready to trade! 🚀** Just get one API key from the providers above and run the forex agent.
