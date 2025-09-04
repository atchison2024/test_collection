import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# General Questions Section
def general_info():
    return dbc.Card([
        dbc.CardHeader("General Information"),
        dbc.CardBody([
            dbc.Form([
                dbc.Label("Amount Being Sought (AUD)"),
                dbc.Input(type="number", id="loan-amount"),

                dbc.Label("Brief Project Description", className="mt-3"),
                dbc.Textarea(id="project-description"),

                dbc.Label("Expected Maturity Date", className="mt-3"),
                dbc.Input(type="date", id="maturity-date"),

                dbc.Label("Repayment Frequency", className="mt-3"),
                dcc.Dropdown(
                    id="repayment-frequency",
                    options=[
                        {"label": opt, "value": opt} for opt in [
                            "Monthly interest only",
                            "Monthly principal and interest",
                            "Quarterly interest",
                            "Interest capitalised",
                            "Bullet/Balloon repayment at maturity",
                            "Custom schedule"
                        ]
                    ],
                    placeholder="Select repayment frequency"
                ),

                dbc.Label("Mortgage Rank", className="mt-3"),
                dcc.Dropdown(
                    id="mortgage-rank",
                    options=[
                        {"label": opt, "value": opt} for opt in [
                            "First Mortgage",
                            "Second Mortgage",
                            "Mezzanine"
                        ]
                    ],
                    placeholder="Select mortgage rank"
                )
            ])
        ])
    ], className="mb-4")

# Placeholder for borrower-specific sections
def borrower_type_questions():
    return dbc.Card([
        dbc.CardHeader("Borrower Details"),
        dbc.CardBody([
            dbc.Label("Please provide the full legal name of the borrowing entity or individual."),
            dbc.Input(type="text", id="borrower-name"),

            dbc.Label("Select Borrower Type", className="mt-3"),
            dcc.Dropdown(
                id="borrower-type",
                options=[
                    {"label": "Company / Trust", "value": "Company / Trust"},
                    {"label": "Individual", "value": "Individual"},
                    {"label": "Partnership", "value": "Partnership"},
                    {"label": "Other", "value": "Other"}
                ],
                placeholder="Select borrower type"
            ),
            html.Div(id="borrower-dynamic-questions")
        ])
    ], className="mb-4")

@app.callback(
    Output("borrower-dynamic-questions", "children"),
    Input("borrower-type", "value")
)
def render_borrower_questions(borrower_type):
    if borrower_type == "Company / Trust":
        return dbc.Form([
            dbc.Label("Please list the directors, trustees, and beneficial owners behind the entity."),
            dbc.Textarea(id="company-directors"),

            dbc.Label("Does the borrower have any related entities or affiliated projects?", className="mt-3"),
            dbc.Textarea(id="company-related-entities"),

            dbc.Label("Please describe the number and type of past property development projects completed by the entity or its directors.", className="mt-3"),
            dbc.Textarea(id="company-experience"),

            dbc.Label("What are the Net Tangible Assets (NTA) of the sponsor or group supporting the transaction?", className="mt-3"),
            dbc.Input(type="text", id="company-nta"),

            dbc.Label("Will personal or corporate guarantees be provided?", className="mt-3"),
            dbc.Textarea(id="company-guarantees"),
        ])

    elif borrower_type == "Individual":
        return dbc.Form([
            dbc.Label("What is your employment type? (PAYG, Self-Employed, Other)"),
            dbc.Input(type="text", id="individual-employment"),

            dbc.Label("Do you have prior property development or investment experience? If so, please summarise.", className="mt-3"),
            dbc.Textarea(id="individual-experience"),

            dbc.Label("Please provide an overview of your personal assets and liabilities.", className="mt-3"),
            dbc.Textarea(id="individual-assets"),

            dbc.Label("Will you be providing any personal guarantees or additional security?", className="mt-3"),
            dbc.Textarea(id="individual-guarantees"),
        ])

    elif borrower_type == "Partnership":
        return dbc.Form([
            dbc.Label("Who are the partners, and what is each partner’s ownership or profit share?"),
            dbc.Textarea(id="partners-share"),

            dbc.Label("Please provide a copy of the partnership agreement.", className="mt-3"),
            dbc.Input(type="text", id="partnership-agreement", placeholder="Upload file or provide path"),

            dbc.Label("Will the partners be providing joint and several guarantees?", className="mt-3"),
            dbc.Textarea(id="partnership-guarantees"),
        ])

    return html.Div("Select a borrower type to view questions.", className="text-muted mt-2")


# Property Characteristics Section
def property_characteristics():
    return dbc.Card([
        dbc.CardHeader("Property Characteristics"),
        dbc.CardBody([
            dbc.Form([
                dbc.Label("What is the zoning classification? (e.g. R1, B2, Greenfield)"),
                dbc.Input(type="text", id="zoning-classification"),

                dbc.Label("What type of location is the asset in?"),
                dcc.Dropdown(
                    id="asset-location",
                    options=[
                        {"label": x, "value": x} for x in ["Metro", "Regional", "Coastal"]
                    ],
                    placeholder="Select location type"
                ),

                dbc.Label("Asset Category", className="mt-3"),
                dcc.Dropdown(
                    id="asset-category",
                    options=[
                        {"label": x, "value": x} for x in ["Residential", "Commercial", "Industrial", "Development Site"]
                    ],
                    placeholder="Select asset category"
                ),

                html.Div(id="asset-category-questions")
            ])
        ])
    ], className="mb-4")

# Dynamic rendering for asset category questions
@app.callback(
    Output("asset-category-questions", "children"),
    Input("asset-category", "value")
)
def render_asset_category_questions(category):
    if category == "Residential":
        return dbc.Form([
            dbc.Label("Is the property owner-occupied or investment?"),
            dcc.Dropdown(
                id="res-occupancy-status",
                options=[{"label": x, "value": x} for x in ["Owner-Occupied", "Investment"]],
                placeholder="Select occupancy status"
            ),
            dbc.Label("Is the property existing, new, off-the-plan or vacant land?", className="mt-3"),
            dbc.Input(type="text", id="res-property-status")
        ])
    elif category == "Commercial":
        return dbc.Form([
            dbc.Label("Is the property leased or vacant?"),
            dcc.Dropdown(
                id="com-leased-status",
                options=[{"label": x, "value": x} for x in ["Leased", "Vacant"]],
                placeholder="Select lease status"
            ),
            dbc.Label("Please provide lease details (tenant name, lease expiry, rent amount)", className="mt-3"),
            dbc.Textarea(id="com-lease-details"),
            dbc.Label("What is the current passing rent?", className="mt-3"),
            dbc.Input(type="number", id="com-passing-rent"),
            dbc.Label("What is the estimated market rent?", className="mt-3"),
            dbc.Input(type="number", id="com-market-rent"),
            dbc.Label("What is the capitalisation rate used in valuation?", className="mt-3"),
            dbc.Input(type="text", id="com-cap-rate")
        ])
    elif category == "Industrial":
        return dbc.Form([
            dbc.Label("Has the land been approved for the proposed industrial use?"),
            dbc.Input(type="text", id="ind-approval"),
            dbc.Label("Has a contamination report been completed for the site?", className="mt-3"),
            dbc.Input(type="text", id="ind-contamination"),
            dbc.Label("Is the facility designed for general warehousing or a specialised use?", className="mt-3"),
            dbc.Input(type="text", id="ind-facility-use"),
            dbc.Label("Is the site located in a metro, regional, or industrial park area?", className="mt-3"),
            dbc.Input(type="text", id="ind-location-type"),
            dbc.Label("What is the estimated total project cost, including contingency?", className="mt-3"),
            dbc.Input(type="number", id="ind-project-cost"),
            dbc.Label("Does the property have adequate access for trucks or machinery?", className="mt-3"),
            dbc.Input(type="text", id="ind-access")
        ])
    elif category == "Development Site":
        return dbc.Form([
            dbc.Label("Has a Development Application been approved?"),
            dbc.Input(type="text", id="dev-da-approved"),
            dbc.Label("What is the estimated Gross Realisation Value (GRV)?", className="mt-3"),
            dbc.Input(type="number", id="dev-grv"),
            dbc.Label("Are there any presales or leasing pre-commitments?", className="mt-3"),
            dbc.Input(type="text", id="dev-presales")
        ])
    return html.Div()


# Loan Purpose Section
def loan_purpose():
    return dbc.Card([
        dbc.CardHeader("Loan Purpose"),
        dbc.CardBody([
            dbc.Form([
                dbc.Label("Select Loan Purpose"),
                dcc.Dropdown(
                    id="loan-purpose",
                    options=[
                        {"label": x, "value": x} for x in ["Acquisition", "Construction", "Refinance", "Bridging"]
                    ],
                    placeholder="Select purpose"
                ),
                html.Div(id="loan-purpose-questions")
            ])
        ])
    ], className="mb-4")

# Loan Purpose Callback
def acquisition_questions():
    return dbc.Form([
        dbc.Label("What is the contract purchase price?"),
        dbc.Input(type="number", id="acq-price"),
        dbc.Label("Has the contract been signed?", className="mt-3"),
        dbc.Input(type="text", id="acq-contract-signed"),
        dbc.Label("What is the equity/deposit contributed by the borrower?", className="mt-3"),
        dbc.Input(type="number", id="acq-equity")
    ])

def construction_questions():
    return dbc.Form([
        dbc.Label("Is a fixed-price building contract in place?"),
        dbc.Input(type="text", id="con-fixed-contract"),
        dbc.Label("Who is the builder, and what is their experience?", className="mt-3"),
        dbc.Textarea(id="con-builder-experience"),
        dbc.Label("What is the expected construction start and completion date?", className="mt-3"),
        dbc.Input(type="text", id="con-dates"),
        dbc.Label("Has a Quantity Surveyor been appointed for progress claims?", className="mt-3"),
        dbc.Input(type="text", id="con-qs-appointed")
    ])

def refinance_questions():
    return dbc.Form([
        dbc.Label("Who is the current lender?"),
        dbc.Input(type="text", id="ref-current-lender"),
        dbc.Label("What is the reason for refinancing?", className="mt-3"),
        dbc.Textarea(id="ref-reason"),
        dbc.Label("Has the existing loan been in arrears in the past 12 months?", className="mt-3"),
        dbc.Input(type="text", id="ref-arrears")
    ])

def bridging_questions():
    return dbc.Form([
        dbc.Label("How long is the bridging loan required for?"),
        dbc.Input(type="text", id="bridge-duration"),
        dbc.Label("How will the bridging loan be repaid? (e.g. sale of existing property)", className="mt-3"),
        dbc.Input(type="text", id="bridge-repayment")
    ])

@app.callback(
    Output("loan-purpose-questions", "children"),
    Input("loan-purpose", "value")
)
def display_loan_purpose_questions(purpose):
    if purpose == "Acquisition":
        return acquisition_questions()
    elif purpose == "Construction":
        return construction_questions()
    elif purpose == "Refinance":
        return refinance_questions()
    elif purpose == "Bridging":
        return bridging_questions()
    return html.Div()

# Credit Structure and Security Section
def credit_structure():
    return dbc.Card([
        dbc.CardHeader("Credit Structure and Security"),
        dbc.CardBody([
            dbc.Form([
                dbc.Label("What is the proposed loan amount?"),
                dbc.Input(type="number", id="credit-loan-amount"),

                dbc.Label("What is the estimated Loan-to-Value Ratio (LVR)?", className="mt-3"),
                dbc.Input(type="number", id="lvr-input"),

                html.Div(id="arbitrage-question"),

                dbc.Label("What valuation method is being used? (As If Complete, GRV)", className="mt-3"),
                dbc.Input(type="text", id="valuation-method"),

                dbc.Label("Is the interest rate fixed or variable?", className="mt-3"),
                dcc.Dropdown(
                    id="rate-type",
                    options=[
                        {"label": "Fixed", "value": "Fixed"},
                        {"label": "Variable", "value": "Variable"}
                    ],
                    placeholder="Select rate type"
                ),

                dbc.Label("Will interest be prepaid or capitalised?", className="mt-3"),
                dcc.Dropdown(
                    id="interest-structure",
                    options=[
                        {"label": "Prepaid", "value": "Prepaid"},
                        {"label": "Capitalised", "value": "Capitalised"}
                    ],
                    placeholder="Select interest payment type"
                ),

                dbc.Label("What type of security will be provided? (1st mortgage, 2nd mortgage, etc.)", className="mt-3"),
                dbc.Input(type="text", id="security-type"),

                dbc.Label("Will full security documents be executed at settlement?", className="mt-3"),
                dbc.Input(type="text", id="security-docs"),

                dbc.Label("Will preferred equity be part of the funding stack?", className="mt-3"),
                dbc.Input(type="text", id="preferred-equity"),

                dbc.Label("Is there an agreement for lease or pre-commitment from a future tenant?", className="mt-3"),
                dbc.Input(type="text", id="precommitment"),

                dbc.Label("What is the primary exit strategy (e.g. refinance to income-producing loan, sale to investor)?", className="mt-3"),
                dbc.Input(type="text", id="exit-strategy"),

                dbc.Label("Has the sponsor delivered similar industrial projects before? If so, please provide details.", className="mt-3"),
                dbc.Textarea(id="sponsor-experience")
            ])
        ])
    ], className="mb-4")

@app.callback(
    Output("arbitrage-question", "children"),
    Input("lvr-input", "value")
)
def show_arbitrage_question(lvr):
    if lvr and lvr > 60:
        return dbc.FormGroup([
            dbc.Label("Is the loan benefiting from a rate offer arbitrage against market averages?"),
            dbc.Input(type="text", id="rate-arbitrage")
        ])
    return html.Div()


# Success and Error Modals
success_modal = dbc.Modal([
    dbc.ModalHeader("Submission Status"),
    dbc.ModalBody("Form submitted successfully!"),
    dbc.ModalFooter(
        dbc.Button("Close", id="close-success", className="ms-auto", n_clicks=0)
    )
], id="success-modal", is_open=False)

error_modal = dbc.Modal([
    dbc.ModalHeader("Submission Error"),
    dbc.ModalBody("There are required fields that have not been filled in."),
    dbc.ModalFooter(
        dbc.Button("Close", id="close-error", className="ms-auto", n_clicks=0)
    )
], id="error-modal", is_open=False)



# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("KeyInvest Application Form", className="mt-4 mb-4 text-center"),
            general_info(),
            borrower_type_questions(),
            property_characteristics(),
            loan_purpose(),
            credit_structure(),
            dbc.Button("Submit", id="submit-button", color="primary", className="mt-3"),
            success_modal,
            error_modal
        ], width=10)
    ], justify="center")
], fluid=True)

# Submission validation and modal callback
# Submission validation and modal callback
@app.callback(
    Output("success-modal", "is_open"),
    Output("error-modal", "is_open"),
    Input("submit-button", "n_clicks"),
    Input("close-success", "n_clicks"),
    Input("close-error", "n_clicks"),
)
def handle_submit(submit, close_success, close_error):
    triggered_id = ctx.triggered_id if ctx.triggered_id else None

    if triggered_id == "close-success":
        return False, False
    if triggered_id == "close-error":
        return False, False
    if triggered_id == "submit-button":
        return False, True
    return False, False


if __name__ == '__main__':
    app.run_server(debug=True)
