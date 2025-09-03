// server.js
const express = require('express');
const bodyParser = require('body-parser');
const { Octokit } = require("@octokit/rest");

const app = express();
app.use(bodyParser.json());

const octokit = new Octokit({ auth: "YOUR_GITHUB_TOKEN" });
const owner = "your-github-username";
const repo = "your-repo-name";

app.post("/api/save", async (req, res) => {
  const { name, age, hobby, timestamp } = req.body;
  const content = `Name: ${name}\nAge: ${age}\nHobby: ${hobby}\nTime: ${timestamp}`;
  const path = `submissions/${Date.now()}.txt`;

  try {
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message: `New submission from ${name}`,
      content: Buffer.from(content).toString('base64'),
      committer: {
        name: "Form Bot",
        email: "form-bot@example.com"
      },
      author: {
        name: "Form Bot",
        email: "form-bot@example.com"
      }
    });
    res.status(200).send("Saved to GitHub.");
  } catch (err) {
    console.error(err);
    res.status(500).send("GitHub error");
  }
});

app.listen(3000, () => console.log("Server running on port 3000"));
