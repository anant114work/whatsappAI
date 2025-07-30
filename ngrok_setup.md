# Making Your Webhook Public with ngrok

## Step 1: Install ngrok
1. Download ngrok from https://ngrok.com/
2. Extract and place ngrok.exe in your system PATH

## Step 2: Start ngrok tunnel
```bash
ngrok http 3000
```

## Step 3: Copy the public URL
You'll get something like: `https://abc123.ngrok.io`

## Step 4: Update Tata Telecom Integration
Use the ngrok URL in your integration:
- **URL**: `https://abc123.ngrok.io/webhook`

## Step 5: Test the webhook
Visit: `https://abc123.ngrok.io/` to see if it shows your bot status

## Alternative: Use your domain
If you have a domain, deploy to:
- Heroku
- AWS
- DigitalOcean
- Any cloud provider

Then use: `https://yourdomain.com/webhook`