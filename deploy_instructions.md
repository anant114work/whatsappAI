# Deploy to Render.com

## Steps:

1. **Create GitHub repo** with all these files
2. **Go to render.com** and sign up
3. **Connect GitHub** and select your repo
4. **Use these settings:**
   - Name: `whatsapp-openai-bot`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

## Your URL will be:
`https://whatsapp-openai-bot.onrender.com`

## For Tata Panel:
- **URL:** `https://whatsapp-openai-bot.onrender.com/webhook`
- **Method:** POST
- **Content-Type:** application/json
- **Body Type:** JSON
- **Body:**
```json
{
  "from": "{{phone}}",
  "text": {
    "body": "{{message}}"
  }
}
```

## Test URLs:
- Home: `https://whatsapp-openai-bot.onrender.com/`
- Status: `https://whatsapp-openai-bot.onrender.com/status`
- Webhook: `https://whatsapp-openai-bot.onrender.com/webhook`