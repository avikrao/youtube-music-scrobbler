const fs = require("fs");
const express = require('express')
const app = express()
const port = process.env.port || process.env.PORT || 80;
const { exec } = require("child_process");

// exec("docker ps -a", (error, stdout, stderr) => {
//   if (error) {
//     console.log(`error: ${error.message}`);
//     return;
//   }
//   if (stderr) {
//       console.log(`stderr: ${stderr}`);
//       return;
//   }
//   console.log(`stdout: ${stdout}`);
// });

app.get('/', (req, res) => {
  const file = fs.readFileSync("/data/scrobblelog.json");
  const data = JSON.parse(file);
  res.json(data);
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
