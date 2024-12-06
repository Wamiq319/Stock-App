from app import create_app, db

# Create the Flask app instance
app = create_app()
 
# Ensure the tables are created before running the app
with app.app_context():
    db.create_all()  # This will create all the tables if they don't exist

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
