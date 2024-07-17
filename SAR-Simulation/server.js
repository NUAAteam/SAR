const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const simulate = require('./simulate');
const sar = require('./SAR');

const app = express();
const PORT = 3000;

app.use(express.static('public'));

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

const upload = multer({ storage });

app.post('/upload', upload.array('images'), (req, res) => {
  res.send('Files uploaded successfully');
});

app.post('/simulate', (req, res) => {
  const { fileName, action } = req.body;
  const filePath = path.join(__dirname, 'uploads', fileName);

  if (action === 'high_res_sar') {
    const result = sar(filePath);
    res.send(result);
  } else if (action === 'strike_effect') {
    const result = simulate(filePath);
    res.send(result);
  }
});

app.get('/download', (req, res) => {
  const zipPath = path.join(__dirname, 'results', 'results.zip');
  res.download(zipPath);
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
