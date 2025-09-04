import dash
from dash import dcc, html, Input, Output

app = dash.Dash(__name__)

# 👇 Add this line to expose the Flask server instance for Gunicorn
server = app.server

# Rest of your layout and callbacks
app.layout = html.Div([
    html.H2('Borrower Information Questionnaire'),

    html.Label('Select Borrower Type:'),
    dcc.Dropdown(
        id='borrower-type',
        options=[
            {'label': 'Company / Trust', 'value': 'Company / Trust'},
            {'label': 'Individual', 'value': 'Individual'},
            {'label': 'Partnership', 'value': 'Partnership'},
        ],
        placeholder="Select borrower type"
    ),

    html.Div(id='dynamic-questions')
])

questions = {
    'Company / Trust': [
        html.Label('Company Name:'),
        dcc.Input(type='text', id='company-name'),

        html.Label('ABN or ACN:'),
        dcc.Input(type='text', id='abn'),

        html.Label('Trustee Name (if trust):'),
        dcc.Input(type='text', id='trustee-name'),
    ],
    'Individual': [
        html.Label('Full Name:'),
        dcc.Input(type='text', id='full-name'),

        html.Label('Date of Birth:'),
        dcc.Input(type='date', id='dob'),

        html.Label('Driver’s Licence Number:'),
        dcc.Input(type='text', id='licence'),
    ],
    'Partnership': [
        html.Label('Partnership Name:'),
        dcc.Input(type='text', id='partnership-name'),

        html.Label('Names of All Partners:'),
        dcc.Textarea(id='partners', placeholder='List all partners here'),

        html.Label('Partnership ABN:'),
        dcc.Input(type='text', id='partnership-abn'),
    ]
}

@app.callback(
    Output('dynamic-questions', 'children'),
    Input('borrower-type', 'value')
)
def display_questions(borrower_type):
    if borrower_type is None:
        return html.Div("Please select a borrower type to view questions.")
    return html.Div(questions[borrower_type])

if __name__ == '__main__':
    app.run_server(debug=True)
