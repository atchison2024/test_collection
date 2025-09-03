import os
html.Label("Age"),
dcc.Input(id="age", type="number", placeholder="Age", style={"width": "100%"}),
html.Br(), html.Br(),
html.Label("Hobby"),
dcc.Input(id="hobby", type="text", placeholder="Hobby", style={"width": "100%"}),
html.Br(), html.Br(),
html.Button("SUBMIT", id="submit", n_clicks=0),
html.Div(id="submit-status", style={"marginTop": "12px"}),
]),
],
)




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
# already authed, show form
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


# Basic validation
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
