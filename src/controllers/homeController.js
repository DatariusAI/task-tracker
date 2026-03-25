const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const getHome = (req, res) => {
  res.json({ message: 'DataariusAI API is running' });
};

module.exports = { getHome };
