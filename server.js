const express = require("express");
const fetch = require("node-fetch");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.post("/api/submit", async (req, res) => {
  const { name, email } = req.body;

  const content = {
    name,
    email,
    timestamp: new Date().toISOString()
  };

  const fileContent = Buffer.from(JSON.stringify(content, null, 2)).toString("base64");

  const response = await fetch("https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/contents/data/" + `${Date.now()}.json`, {
    method: "PUT",
    headers: {
      "Authorization": `token ${process.env.GITHUB_TOKEN}`,
      "Accept": "application/vnd.github.v3+json"
    },
    body: JSON.stringify({
      message: "New form submission",
      content: fileContent,
      branch: "main"
    })
  });

  if (response.ok) {
    res.json({ message: "Submitted successfully!" });
  } else {
    const error = await response.json();
    res.status(500).json({ message: "GitHub API error", error });
  }
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
