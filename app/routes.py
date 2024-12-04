from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from app import db
from app.models import StockList, Timeframe

# Define the Blueprint
bp = Blueprint('main', __name__)

# Route to get the stock list and timeframe, or save them on POST
@bp.route('/', methods=['GET', 'POST'])
def home():
    stock_data = []
    if request.method == "POST":
        stock_list = request.form.get("stock-list")
        time_frame = request.form.get("time-frame")
        
        # Example data based on selection (in real use, this will be fetched from a database or API)
        stock_data = [
            {"symbol": "AAPL", "time_frame": time_frame, "price": "$150.00", "indicator": "RSI: 70"},
            {"symbol": "GOOG", "time_frame": time_frame, "price": "$2800.00", "indicator": "MACD: 1.5"},
        ]
        
    return render_template("home.html", stock_data=stock_data)

@bp.route('/stock-list', methods=['GET'])
def stock_list():
    # Fetch all stocks from the database to display
    stocks = [
        {
            "name": "Technology Stocks",
            "symbols": ["AAPL", "GOOG", "MSFT"]
        },
        {
            "name": "Healthcare Stocks",
            "symbols": ["JNJ", "PFE"]
        },
        {
            "name": "Energy Stocks",
            "symbols": ["XOM", "CVX"]
        }
    ]

    return render_template('stock_list.html', stocks=stocks)

from flask import render_template, request, redirect

@bp.route('/create-stock', methods=['GET', 'POST'])
def create_stock():
    if request.method == 'POST':
        stock_name = request.form['stock-list-name']
        symbols = [request.form[f'stock-symbol-{i}'] for i in range(1, 10) if request.form[f'stock-symbol-{i}']]
        
        # Add stock to the database (this step is missing in your current code)
        # Assuming you have a function to add to DB, like `add_stock(stock_name, symbols)`
        
        # Redirect to the stock list after form submission
        return redirect('/stock-list')
    
    # Create an empty stock object for the form when it's not a POST request
    stock = {
        'name': '',
        'symbols': [''] * 9,  # Empty symbols for 9 stock symbols
        'last_updated': None
    }

    return render_template('stock_form.html', is_update=False, stock=stock)


@bp.route('/update-stock/<int:stock_id>', methods=['GET', 'POST'])
def update_stock(stock_id):
    stock = get_stock_by_id(stock_id)  # Fetch stock from database
    if request.method == 'POST':
        stock_name = request.form['stock-list-name']
        symbols = [request.form[f'stock-symbol-{i}'] for i in range(1, 11) if request.form[f'stock-symbol-{i}']]
        # Update stock in the database
        return redirect('/stock-list')
    return render_template('stock_form.html', is_update=True, stock=stock)

from flask import render_template

@bp.route('/indicator-results', methods=['GET', 'POST'])
def indicator_results():
    # Dummy data for testing
    indicator_results = [
        {"symbol": "AAPL", "date": "2024-12-01", "indicator_value": 150},
        {"symbol": "GOOG", "date": "2024-12-01", "indicator_value": 1250},
        {"symbol": "AMZN", "date": "2024-12-01", "indicator_value": 3500},
    ]
    
    selected_stock_list = "Stock List 1"  # Example static value for testing

    return render_template('indicator_results.html', indicator_results=indicator_results, selected_stock_list=selected_stock_list)
