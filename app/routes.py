from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Route for Home page
@main.route('/')
def home():
    return render_template('home.html')

# Route for results page where the indicator is passed dynamically
@main.route('/results/<indicator>')
def results(indicator):
    # Assuming the indicator data is based on the type of indicator passed
    indicator_data = get_indicator_data(indicator)
    return render_template('results.html', indicator=indicator, data=indicator_data)

# Function to simulate getting the data based on the indicator
def get_indicator_data(indicator):
    # Here, you'll retrieve the data for the specific indicator
    # This is just an example; replace with your actual data fetching logic
    if indicator == "rsi":
        return {"value": "70", "status": "Overbought"}
    elif indicator == "mcad":
        return {"value": "Positive", "status": "Buy"}
    elif indicator == "adi":
        return {"value": "40", "status": "Rising"}
    else:
        return {"value": "N/A", "status": "No data"}
