const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic();

const sessions = {};

router.get('/', homeController.getHome);

router.post('/chat', async (req, res) => {
  const { message, sessionId } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  const id = sessionId || 'default';

  if (!sessions[id]) {
    sessions[id] = [];
  }

  sessions[id].push({ role: 'user', content: message });

  try {
    const response = await client.messages.create({
      model: 'claude-sonnet-4-5',
      max_tokens: 1024,
      messages: sessions[id],
    });

    const reply = response.content[0].text;

    sessions[id].push({ role: 'assistant', content: reply });

    res.json({ reply, sessionId: id });
  } catch (err) {
    console.error('Claude API error:', err);
    res.status(500).json({ error: 'Claude API call failed' });
  }
});

module.exports = router;
