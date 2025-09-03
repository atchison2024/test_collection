import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import os

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
    
    return "Information submitted successfully."

if __name__ == '__main__':
    app.run_server(debug=True)
