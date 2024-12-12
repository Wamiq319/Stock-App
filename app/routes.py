from flask import Blueprint, request, flash, render_template, redirect, url_for
from . import db
from .models import StockList
from app.utils.stocks_utils import fetch_stock_data
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

    try:
        if request.method == 'POST':
            data = request.form
            stock_list_id = data.get('stock-list')
            time_frame = data.get('time-frame')
            selected_stock_list = StockList.query.filter_by(id=stock_list_id).first()
            stocks = selected_stock_list.stocks.split(',')

            logger.info("Fetching stock data (home route)")
            fetch_stock_data("IBM", time_frame)

    except Exception as e:
        logger.error(" Error fetching stock data: {e}")
        flash("Failed to fetch stock data", "error")

    return render_template("home.html", stock_lists=stock_lists, indicators_result=None)

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

@bp.route('/stock-list', methods=['GET'])
def stock_list():
    try:
        stock_groups = [
            {
                'id': stock_list.id,
                'name': stock_list.name,
                'stocks': stock_list.stocks.split(',') if stock_list.stocks else []
            }
            for stock_list in StockList.query.all()
        ]
        logger.info(f"(stock-list route) Prepared {len(stock_groups)} stock groups")
    except Exception as e:
        logger.error(f"(stock-list route) Error preparing stock list: {e}")
        stock_groups = []

    return render_template('stock_list.html', stock_lists=stock_groups)

@bp.route('/indicator-results', methods=['GET', 'POST'])
def indicator_results():
    indicator_results = [
        {"symbol": "AAPL", "date": "2024-12-01", "indicator_value": 150},
        {"symbol": "GOOG", "date": "2024-12-01", "indicator_value": 1250},
        {"symbol": "AMZN", "date": "2024-12-01", "indicator_value": 3500},
    ]
    selected_stock_list = "Stock List 1"
    logger.info(f"(indicator-results route) Displaying results for {selected_stock_list}")

    return render_template('indicator_results.html', indicator_results=indicator_results, selected_stock_list=selected_stock_list)
