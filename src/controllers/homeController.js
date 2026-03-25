const getHome = (req, res) => {
  res.json({ message: 'DatariusAI is running' });
};

module.exports = { getHome };
