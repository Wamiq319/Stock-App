from app import db

# Stock List model
class StockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    symbols = db.Column(db.String(500), nullable=False)  # List of stock symbols as a comma-separated string

    def __repr__(self):
        return f'<Stock List {self.name}>'

# Timeframe model associated with a stock list
class Timeframe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_list_id = db.Column(db.Integer, db.ForeignKey('stock_list.id'), nullable=False)
    timeframe = db.Column(db.String(20), nullable=False)

    stock_list = db.relationship('StockList', backref=db.backref('timeframes', lazy=True))

    def __repr__(self):
        return f'<Timeframe {self.timeframe} for {self.stock_list.name}>'
