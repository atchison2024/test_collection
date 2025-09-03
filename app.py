import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import os

import base64
import requests
from datetime import datetime

# Replace with your values
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = 'atchison2024'
REPO_NAME = 'test_collection'
FILE_PATH = 'submissions.csv'  # relative path in the repo
BRANCH = 'main'

def push_csv_to_github(csv_path_local):
    with open(csv_path_local, 'rb') as f:
        content = f.read()
        encoded_content = base64.b64encode(content).decode('utf-8')

    # Get SHA if file exists (needed for update)
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        sha = None

    commit_message = f"Update submissions.csv at {datetime.utcnow().isoformat()}"

    data = {
        'message': commit_message,
        'content': encoded_content,
        'branch': BRANCH,
    }

    if sha:
        data['sha'] = sha  # needed if updating

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print("✅ File successfully pushed to GitHub.")
    else:
        print(f"❌ Failed to push file: {response.status_code}")
        print(response.json())

# Initialize the app
app = dash.Dash(__name__)
server = app.server  # For deployment

# Password value to access the form
CORRECT_PASSWORD = '123456'

# Layout with conditional content
app.layout = html.Div([
    dcc.Store(id='authenticated', data=False),
    
    html.Div(id='auth-container', children=[
        html.H2("Enter Password to Access Form"),
        dcc.Input(id='password-input', type='password', placeholder='Enter password'),
        html.Button('Submit Password', id='submit-password', n_clicks=0),
        html.Div(id='password-message')
    ]),
    
    html.Div(id='form-container', style={'display': 'none'}, children=[
        html.H2("Submit Your Info"),
        dcc.Input(id='name-input', type='text', placeholder='Enter Name'),
        dcc.Input(id='age-input', type='number', placeholder='Enter Age'),
        dcc.Input(id='hobby-input', type='text', placeholder='Enter Hobby'),
        html.Button('Submit', id='submit-form', n_clicks=0),
        html.Div(id='form-message')
    ])
])

@app.callback(
    Output('authenticated', 'data'),
    Output('password-message', 'children'),
    Input('submit-password', 'n_clicks'),
    State('password-input', 'value'),
    prevent_initial_call=True
)
def verify_password(n_clicks, password):
    if password == CORRECT_PASSWORD:
        return True, "Access granted."
    else:
        return False, "Incorrect password."

@app.callback(
    Output('auth-container', 'style'),
    Output('form-container', 'style'),
    Input('authenticated', 'data')
)
def toggle_layout(authenticated):
    if authenticated:
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {'display': 'block'}, {'display': 'none'}

@app.callback(
    Output('form-message', 'children'),
    Input('submit-form', 'n_clicks'),
    State('name-input', 'value'),
    State('age-input', 'value'),
    State('hobby-input', 'value'),
    prevent_initial_call=True
)
def submit_form(n_clicks, name, age, hobby):
    if not name or not age or not hobby:
        return "Please fill in all fields."

    new_data = pd.DataFrame([{
        'Name': name,
        'Age': age,
        'Hobby': hobby
    }])

    file_path = 'submissions.csv'
    
    if os.path.exists(file_path):
        new_data.to_csv(file_path, mode='a', header=False, index=False)
    else:
        new_data.to_csv(file_path, index=False)
        
    push_csv_to_github("submissions.csv")
    
    return "Information submitted successfully."

if __name__ == '__main__':
    app.run_server(debug=True)
