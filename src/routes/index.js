const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

router.get('/', homeController.getHome);

router.post('/chat', async (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  try {
    const response = await client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1024,
      messages: [{ role: 'user', content: message }],
    });

    res.json({ reply: response.content[0].text });
  } catch (err) {
    console.error('Claude API error:', err);
    res.status(500).json({ error: 'Claude API call failed' });
  }
});

module.exports = router;
