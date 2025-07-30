const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());

const WHATSAPP_TOKEN = process.env.WHATSAPP_TOKEN;
const WHATSAPP_PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

// Webhook verification
app.get('/webhook', (req, res) => {
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode === 'subscribe' && token === VERIFY_TOKEN) {
        console.log('Webhook verified');
        res.status(200).send(challenge);
    } else {
        res.sendStatus(403);
    }
});

// Handle incoming messages
app.post('/webhook', async (req, res) => {
    const body = req.body;

    if (body.object === 'whatsapp_business_account') {
        body.entry.forEach(async (entry) => {
            const changes = entry.changes;
            changes.forEach(async (change) => {
                if (change.field === 'messages') {
                    const messages = change.value.messages;
                    if (messages) {
                        for (const message of messages) {
                            await handleMessage(message, change.value.contacts[0]);
                        }
                    }
                }
            });
        });
        res.status(200).send('OK');
    } else {
        res.sendStatus(404);
    }
});

// Handle individual message
async function handleMessage(message, contact) {
    const from = message.from;
    const messageText = message.text?.body;

    if (messageText) {
        console.log(`Received message from ${contact.profile.name}: ${messageText}`);
        
        try {
            // Get AI response from OpenAI
            const aiResponse = await getOpenAIResponse(messageText);
            
            // Send reply via WhatsApp
            await sendWhatsAppMessage(from, aiResponse);
        } catch (error) {
            console.error('Error processing message:', error);
            await sendWhatsAppMessage(from, 'Sorry, I encountered an error. Please try again.');
        }
    }
}

// Get response from OpenAI
async function getOpenAIResponse(userMessage) {
    try {
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-3.5-turbo',
            messages: [
                {
                    role: 'system',
                    content: 'You are a helpful WhatsApp assistant. Keep responses concise and friendly.'
                },
                {
                    role: 'user',
                    content: userMessage
                }
            ],
            max_tokens: 150,
            temperature: 0.7
        }, {
            headers: {
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        return response.data.choices[0].message.content.trim();
    } catch (error) {
        console.error('OpenAI API error:', error.response?.data || error.message);
        throw error;
    }
}

// Send message via WhatsApp Business API
async function sendWhatsAppMessage(to, message) {
    try {
        const response = await axios.post(
            `https://graph.facebook.com/v18.0/${WHATSAPP_PHONE_NUMBER_ID}/messages`,
            {
                messaging_product: 'whatsapp',
                to: to,
                text: { body: message }
            },
            {
                headers: {
                    'Authorization': `Bearer ${WHATSAPP_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        console.log('Message sent successfully');
    } catch (error) {
        console.error('WhatsApp API error:', error.response?.data || error.message);
        throw error;
    }
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});