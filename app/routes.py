from flask import Blueprint, request, jsonify,flash, render_template, redirect, url_for
from . import db
from .models import StockList
from app.utils.stocks_utils import fetch_stock_data
from app.utils.indicators_utils import calculate_rsi,calculate_adx,calculate_macd
from . import setup_logger


bp = Blueprint('stocks', __name__)

logger = setup_logger("ROUTES")

@bp.route('/', methods=['GET', 'POST'])
def home():
    stock_lists = [
        {
            'id': stock_list.id,
            'name': stock_list.name,
            'total_stocks': len(stock_list.stocks.split(',')) if stock_list.stocks else 0
        }
        for stock_list in StockList.query.all()
        if stock_list.stocks and len(stock_list.stocks.split(',')) > 0
    ]

    Data = None  # Initialize Data outside try-catch so it always exists.

    try: 
        if request.method == 'POST':
            data = request.form
            
            stock_list_id = data.get('stock-list')
            time_frame = data.get('time-frame')
            selected_stock_list = StockList.query.filter_by(id=stock_list_id).first()
            stocks = selected_stock_list.stocks.split(',')

            # Initialize Data in POST request
            Data = [{"stock_list_name": selected_stock_list.name, "time_frame": time_frame}]
            
            for stock_symbol in stocks:
                Stock_Data = fetch_stock_data(stock_symbol, time_frame)
                rsi_values = calculate_rsi(Stock_Data)
                macd_values = calculate_macd(Stock_Data)
                adx_values = calculate_adx(Stock_Data)
                most_recent_data = Stock_Data.iloc[0]
                print(most_recent_data)
                recent_data = {
                    'timestamp': most_recent_data['UTC-time-zone'], 
                    'high': int(most_recent_data['High']), 
                    'low': int(most_recent_data['Low']),   
                    'close': int(most_recent_data['Close']),  
                    'open': int(most_recent_data['Open']),   
                    'volume': int(most_recent_data['Volume'])  
                }
                
                Data.append({
                    "symbol": stock_symbol, 
                    "rsi": rsi_values, 
                    "macd": macd_values, 
                    "adx": adx_values, 
                    "recent_data": recent_data
                })
                
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        flash("Failed to fetch stock data", "error")
        Data = None  # Ensure Data is set to None if there’s an error

    # Return the template with stock_lists and Data
    return render_template("home.html", stock_lists=stock_lists, Data=Data)


@bp.route('/create-stock', methods=['GET', 'POST'])
def create_or_update_stock():
    error = False
    stock = None

    if 'stock-id' in request.args:
        stock_id = request.args.get('stock-id')
        stock = StockList.query.get(stock_id)
        if not stock:
            flash("Stock list not found", "error")
            logger.warning("Stock list not found")
            return redirect(url_for('stocks.create_or_update_stock'))

    if request.method == 'POST':
        stock_list_name = request.form['stock-list-name']
        logger.info(f"(create-stock route) Creating/updating stock list: {stock_list_name}")

        existing_stock_list = StockList.query.filter_by(name=stock_list_name).first()
        if existing_stock_list and existing_stock_list.id != (stock.id if stock else None):
            flash("Stock list name already exists", "error")
            logger.warning(f"(create-stock route) Duplicate stock list name: {stock_list_name}")
            error = True

        symbols = [request.form.get(f'stock-symbol-{i}') for i in range(1, 10) if request.form.get(f'stock-symbol-{i}')]
        if not symbols:
            flash("At least one stock symbol is required", "error")
            logger.warning("(create-stock route) No stock symbols provided")
            error = True

        if error:
            return render_template('stock_form.html', stock=stock, is_update=bool(stock))

        symbols = [symbol.upper() for symbol in symbols]
        stock_list_name = stock_list_name.upper()

        try:
            if stock:
                stock.name = stock_list_name
                stock.stock_symbols = symbols
                logger.info(f"(create-stock route) Updated stock list: {stock_list_name}")
            else:
                stock = StockList(name=stock_list_name, stock_symbols=symbols)
                db.session.add(stock)
                logger.info(f"(create-stock route) Created new stock list: {stock_list_name}")

            db.session.commit()
            flash("Stock list created/updated successfully", "success")
        except Exception as e:
            logger.error(f"(create-stock route) Error saving stock list: {e}")
            flash("Error creating/updating stock list", "error")

        return render_template('stock_form.html', stock=stock, is_update=True)

    return render_template('stock_form.html', stock=stock, is_update=bool(stock))


@bp.route('/stock-list', methods=['GET', 'POST'])
def stock_list():
    try:
        # Handle GET request: Fetch all stock lists
        if request.method == 'GET':
            stock_groups = [
                {
                    'id': stock_list.id,
                    'name': stock_list.name,
                    'stocks': stock_list.stocks.split(',') if stock_list.stocks else []
                }
                for stock_list in StockList.query.all()
            ]
            logger.info(f"(stock-list route) Prepared {len(stock_groups)} stock groups")
            return render_template('stock_list.html', stock_lists=stock_groups)

        # Handle POST request for deleting a stock list
        if request.method == 'POST':
            stock_id = request.form.get('stockId')  # Get stock list ID from form data
            stock_list = StockList.query.get(stock_id)  # Query the database for the stock list

            if stock_list:
                db.session.delete(stock_list)  # Delete the stock list from the database
                db.session.commit()
                flash(f"Stock list '{stock_list.name}' deleted successfully.", "success")
                logger.info(f"(stock-list route) Deleted stock list with ID: {stock_id}")
            else:
                flash(f"Stock list with ID {stock_id} not found.", "error")
                logger.error(f"(stock-list route) Stock list with ID {stock_id} not found.")

            return redirect(url_for('stocks.stock_list'))

    except Exception as e:
        logger.error(f"(stock-list route) Error handling stock list request: {e}")
        flash('An error occurred while processing your request.', 'error')
        return redirect(url_for('stocks.stock_list'))

@bp.route('/indicator-results', methods=['GET', 'POST'])
def indicator_results():
    stock_lists = [
        {
            'id': stock_list.id,
            'name': stock_list.name,
            'total_stocks': len(stock_list.stocks.split(',')) if stock_list.stocks else 0
        }
        for stock_list in StockList.query.all()
        if stock_list.stocks and len(stock_list.stocks.split(',')) > 0
    ]

    Data = None  # Initialize Data outside try-catch so it always exists.
    if request.method == 'POST':
            data = request.form
            stock_list_id = data.get('stock-list')
            time_frame = data.get('time-frame')
            indicator = data.get('indicator')
            selected_stock_list = StockList.query.filter_by(id=stock_list_id).first()
            stocks = selected_stock_list.stocks.split(',')
            
            # Example Usage
            Data = [{"indicator":indicator, "time_frame": time_frame,"stock_list_name":selected_stock_list.name}]
            for stock_symbol in stocks:
                Stock_Data= fetch_stock_data(stock_symbol, time_frame)
                print(indicator)
                if indicator == 'RSI':
                    rsi_values = calculate_rsi(Stock_Data)
                    Data.append({"symbol": stock_symbol, "indicator": rsi_values})
                elif indicator == 'MACD':
                    macd_values = calculate_macd(Stock_Data) 
                    Data.append({"symbol": stock_symbol, "indicator": macd_values})
                elif indicator == 'ADX':
                    adx_values = calculate_adx(Stock_Data)
                    
                    Data.append({"symbol": stock_symbol, "indicator": adx_values,})
            return render_template("indicator_results.html",stock_lists=stock_lists, Data =Data)

    return render_template("indicator_results.html", stock_lists=stock_lists,Data=None)