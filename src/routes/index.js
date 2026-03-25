const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');


router.get('/', homeController.getHome);


router.post('/chat', (req, res) => {
  const { message } = req.body;

  if (!message) {
    return res.status(400).json({
      error: 'Message is required'
    });
  }

  res.json({
    reply: `You said: ${message}`
  });
});

module.exports = router;
