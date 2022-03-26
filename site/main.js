const fs = require("fs");
const express = require('express')
const handlebars = require("hbs");
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

app.set("views", __dirname);
app.set("view engine", "hbs");

const timestampToString = (timestamp) => {
  return (new Date(Math.floor(timestamp))).toLocaleString("en-US", { timeZone: "America/New_York" });
}

app.get('/', (req, res) => {
  const historyFile = fs.readFileSync("/data/scrobblelog.json"),
    unprocessedHistory = JSON.parse(historyFile),
    history = unprocessedHistory.map(entry => {
      entry.timestamp = timestampToString(entry.timestamp*1000);
      return entry;
    });
  const latestPing = parseFloat(fs.readFileSync("/data/pinglog.txt", 'utf-8'))*1000,
    recent = (Math.abs(new Date(latestPing) - new Date()) / 60000) < 2;

  history.reverse();
  
  res.render("index.hbs", { history, recent, timestamp: timestampToString(latestPing) });
});

app.get("/restart", (req, res) => {
  exec("docker restart -t 2 scrobbler", (error, stdout, stderr) => {
    if (error) {
      console.log(`error: ${error.message}`);
      res.json({"error": error.message});
      return;
    }
    if (stderr) {
        console.log(`stderr: ${stderr}`);
        res.json({"stderr": stderr});
        return;
    }
    console.log(`stdout: ${stdout}`);
    res.json({"stdout": stdout});
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
});
