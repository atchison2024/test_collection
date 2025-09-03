import os
import base64
import csv
from io import StringIO
from datetime import datetime, timezone

import requests
from dash import Dash, html, dcc, callback, Input, Output, State

# ---- Config from environment ----
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD", "123456")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # format: owner/repo
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
DATA_PATH = os.getenv("DATA_PATH", "data/submissions.csv")
COMMITTER_NAME = os.getenv("COMMITTER_NAME")
COMMITTER_EMAIL = os.getenv("COMMITTER_EMAIL")

if not GITHUB_TOKEN:
    print("WARNING: GITHUB_TOKEN not set. Submissions will fail.")
if not GITHUB_REPO or "/" not in (GITHUB_REPO or ""):
    print("WARNING: GITHUB_REPO must be 'owner/repo'. Submissions will fail.")

OWNER, REPO = (GITHUB_REPO.split("/") + [None])[:2] if GITHUB_REPO else (None, None)

API_BASE = f"https://api.github.com/repos/{OWNER}/{REPO}/contents" if OWNER and REPO else None
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}


# ---- GitHub helpers ----
def _get_existing_file(path: str, ref: str):
    """Return (text_content, sha) if file exists, else (None, None)."""
    url = f"{API_BASE}/{path}"
    params = {"ref": ref}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        content_b64 = data.get("content", "")
        text = base64.b64decode(content_b64).decode("utf-8") if content_b64 else ""
        return text, data.get("sha")
    if r.status_code == 404:
        return None, None
    raise RuntimeError(f"GitHub GET failed {r.status_code}: {r.text}")


def _put_file(path: str, content_text: str, message: str, branch: str, sha: str | None):
    url = f"{API_BASE}/{path}"
    payload = {
        "message": message,
        "content": base64.b64encode(content_text.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha
    if COMMITTER_NAME and COMMITTER_EMAIL:
        payload["committer"] = {"name": COMMITTER_NAME, "email": COMMITTER_EMAIL}
    r = requests.put(url, headers=HEADERS, json=payload)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"GitHub PUT failed {r.status_code}: {r.text}")


def append_row_to_repo_csv(path: str, row: dict, branch: str = GITHUB_BRANCH):
    """Append a CSV row to path in the repo. Create file with header if missing."""
    existing_text, sha = _get_existing_file(path, ref=branch)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["timestamp", "name", "age", "hobby"])

    if existing_text is None:
        # File does not exist yet — create with header
        writer.writeheader()
    else:
        output.write(existing_text)
        if not existing_text.endswith("\n"):
            output.write("\n")

    writer.writerow(row)
    new_text = output.getvalue()

    _put_file(
        path=path,
        content_text=new_text,
        message=f"Append submission for {row['name']} at {row['timestamp']}",
        branch=branch,
        sha=sha,
    )


# ---- Dash UI ----
app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"maxWidth": "640px", "margin": "40px auto", "fontFamily": "system-ui, -apple-system, Segoe UI"},
    children=[
        html.H2("Secure Form"),
        dcc.Store(id="authed", data=False),

        # Login section
        html.Div(
            id="login-section",
            children=[
                html.Label("Password"),
                dcc.Input(id="password-input", type="password", placeholder="Enter password", style={"width": "100%"}),
                html.Button("Enter", id="auth-button", n_clicks=0, style={"marginTop": "12px"}),
                html.Div(id="login-status", style={"marginTop": "8px"}),
            ],
        ),

        # Form section
        html.Div(
            id="form-section",
            style={"display": "none", "marginTop": "24px"},
            children=[
                html.Label("Name"),
                dcc.Input(id="name", type="text", placeholder="Full name", style={"width": "100%"}),
                html.Br(), html.Br(),
                html.Label("Age"),
                dcc.Input(id="age", type="number", placeholder="Age", style={"width": "100%"}),
                html.Br(), html.Br(),
                html.Label("Hobby"),
                dcc.Input(id="hobby", type="text", placeholder="Hobby", style={"width": "100%"}),
                html.Br(), html.Br(),
                html.Button("SUBMIT", id="submit", n_clicks=0),
                html.Div(id="submit-status", style={"marginTop": "12px"}),
            ],
        ),
    ],
)


# ---- Callbacks ----
@callback(
    Output("authed", "data"),
    Output("login-status", "children"),
    Output("login-section", "style"),
    Output("form-section", "style"),
    Input("auth-button", "n_clicks"),
    State("password-input", "value"),
    State("authed", "data"),
    prevent_initial_call=True,
)
def do_auth(n_clicks, password, authed):
    if authed:
        return True, "", {"display": "none"}, {"display": "block"}
    if not password:
        return False, "Please enter a password.", {"display": "block"}, {"display": "none"}
    if password == ACCESS_PASSWORD:
        return True, "Authenticated.", {"display": "none"}, {"display": "block"}
    return False, "Incorrect password.", {"display": "block"}, {"display": "none"}


@callback(
    Output("submit-status", "children"),
    Input("submit", "n_clicks"),
    State("authed", "data"),
    State("name", "value"),
    State("age", "value"),
    State("hobby", "value"),
    prevent_initial_call=True,
)
def handle_submit(n_clicks, authed, name, age, hobby):
    if not authed:
        return "Not authenticated."

    name = (name or "").strip()
    hobby = (hobby or "").strip()
    if not name or age is None or not hobby:
        return "Please provide name, age and hobby."

    ts = datetime.now(timezone.utc).isoformat()
    row = {"timestamp": ts, "name": name, "age": int(age), "hobby": hobby}

    try:
        if not (GITHUB_TOKEN and OWNER and REPO):
            return "Server is not configured to save to GitHub."
        append_row_to_repo_csv(DATA_PATH, row)
        return "Submission saved successfully."
    except Exception as e:
        return f"Error saving submission: {e}"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.getenv("PORT", 8050)), debug=False)
