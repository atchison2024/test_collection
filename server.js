const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { Octokit } = require('@octokit/rest');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// GitHub config
const octokit = new Octokit({ auth: "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" });
const owner = "YOUR_GITHUB_USERNAME";
const repo = "YOUR_REPO_NAME";

app.post('/api/save', async (req, res) => {
  const { name, age, hobby, timestamp } = req.body;

  const content = `Name: ${name}\nAge: ${age}\nHobby: ${hobby}\nTime: ${timestamp}`;
  const path = `submissions/${Date.now()}.txt`;

  try {
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message: `Form submission: ${name}`,
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
    res.status(200).send("Saved successfully.");
  } catch (err) {
    console.error(err);
    res.status(500).send("Error saving to GitHub.");
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});
