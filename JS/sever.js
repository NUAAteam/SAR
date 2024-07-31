const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());

let users = [];

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);
  if (user) {
    res.status(200).send('登录成功');
  } else {
    res.status(401).send('用户名或密码错误');
  }
});

app.post('/register', (req, res) => {
  const { username, password } = req.body;
  const userExists = users.some(u => u.username === username);
  if (userExists) {
    res.status(409).send('用户已存在');
  } else {
    users.push({ username, password });
    res.status(201).send('注册成功');
  }
});

app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});