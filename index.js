require('dotenv').config();
const express = require('express');
const app = express();

app.use(express.json());
app.use('/', require('./src/routes/index'));

app.listen(3000, () => {
  console.log('DataariusAI server running on port 3000');
});
```

`.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxx
