from . import db  # Import db from __init__.py

class StockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stocks = db.Column(db.String(100), nullable=False)  # Storing stock symbols as a comma-separated string

    def __init__(self, name, stock_symbols):
        self.name = name
        if len(stock_symbols) <= 9:
            self.stocks = ",".join(stock_symbols)  # Store as a comma-separated string
        else:
            raise ValueError("A maximum of 9 stock symbols are allowed")

    def get_stocks(self):
        return self.stocks.split(",") if self.stocks else []
