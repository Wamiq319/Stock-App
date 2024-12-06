from flask import Blueprint, request, jsonify, render_template, redirect
from . import db
from .models import StockList  # Import the StockList model

bp = Blueprint('stocks', __name__)

# Route to display stock data
@bp.route('/', methods=['GET', 'POST'])
def home():
    stock_data = []
    if request.method == "POST":
        stock_list = request.form.get("stock-list")
        time_frame = request.form.get("time-frame")
        
        # Example data based on stock list and time frame (in real use, fetch from DB or API)
        stock_data = [
            {"symbol": "AAPL", "time_frame": time_frame, "price": "$150.00", "indicator": "RSI: 70"},
            {"symbol": "GOOG", "time_frame": time_frame, "price": "$2800.00", "indicator": "MACD: 1.5"},
        ]
        
    return render_template("home.html", stock_data=stock_data)

# Route to create a new stock list
@bp.route('/create-stock', methods=['GET', 'POST'])
def create_stock():
    if request.method == 'POST':
        stock_name = request.form['stock-list-name']
        
        # Check if stock list name already exists
        existing_stock_list = StockList.query.filter_by(name=stock_name).first()
        if existing_stock_list:
            return jsonify({"error": "Stock list name already exists"}), 400
        
        # Collect stock symbols (only if they are provided)
        symbols = [request.form.get(f'stock-symbol-{i}') for i in range(1, 10) if request.form.get(f'stock-symbol-{i}')]
        if not symbols:
            return jsonify({"error": "At least one stock symbol is required"}), 400

        # Convert all symbols to uppercase
        symbols = [symbol.upper() for symbol in symbols]
        
        # Create the stock list and add to the database
        stock_list = StockList(name=stock_name, stock_symbols=symbols)
        db.session.add(stock_list)
        db.session.commit()

        return jsonify({"message": "Stock list created successfully", "id": stock_list.id}), 201

    return render_template('stock_form.html', is_update=False)  # You can pass `stock` if you need to edit or show existing stock list.

# Route to display stock list grouped by category (Assuming Stock has a category field, adjust accordingly)
@bp.route('/stock-list', methods=['GET'])
def stock_list():
    stocks = StockList.query.all()  # Get all stock lists from the database
    stock_groups = {}

    # Categorize stocks based on their 'category' field (adjust as per DB structure)
    for stock in stocks:
        category = stock.name  # Adjust this if you need to categorize based on another field
        stock_groups.setdefault(category, []).append({
            'id': stock.id,
            'symbol': stock.name
        })
    
    # Prepare stock data for template rendering
    stock_data = [{"name": category, "stocks": symbols} for category, symbols in stock_groups.items()]
    
    return render_template('stock_list.html', stocks=stock_data)

# Route to update an existing stock list
@bp.route('/update-stock/<int:stock_id>', methods=['GET', 'POST'])
def update_stock(stock_id):
    stock = StockList.query.get_or_404(stock_id)  # Fetch stock by ID (or 404 if not found)
    
    if request.method == 'POST':
        stock_name = request.form['stock-list-name']
        symbols = [request.form[f'stock-symbol-{i}'] for i in range(1, 11) if request.form.get(f'stock-symbol-{i}')]
        
        # Update stock in the database
        stock.name = stock_name
        stock.stocks = ",".join([symbol.upper() for symbol in symbols])  # Update symbols as a comma-separated string
        db.session.commit()
        
        return redirect('/stock-list')
    
    return render_template('stock_form.html', is_update=True, stock=stock)

# Route to display indicator results (Example for testing)
@bp.route('/indicator-results', methods=['GET', 'POST'])
def indicator_results():
    # Example data for testing (replace with actual data fetching)
    indicator_results = [
        {"symbol": "AAPL", "date": "2024-12-01", "indicator_value": 150},
        {"symbol": "GOOG", "date": "2024-12-01", "indicator_value": 1250},
        {"symbol": "AMZN", "date": "2024-12-01", "indicator_value": 3500},
    ]
    
    selected_stock_list = "Stock List 1"  # Example static value for testing

    return render_template('indicator_results.html', indicator_results=indicator_results, selected_stock_list=selected_stock_list)
