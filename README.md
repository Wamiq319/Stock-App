# MyExperiment.com Shares (Stock-App)

This is a simple Flask web application that utilizes the **Alpaca API** for stock analysis and displays indicator results you can visist the app here http://13.40.214.188/. This project was built for Steven on Fiverr. The problem statement for the project was as follows:

## Problem Statement
The purpose of this project is to create a website that helps in analyzing investment opportunities and tracking portfolios. The website will have two main functionalities:

1. **Opportunity Analysis**: This will evaluate a variety of technical indicators to identify potential investment opportunities.


The website was developed from scratch, and the IG Index API was suggested by the user to be used initially for fetching stock data. The reason for this choice is that the IG Index API allows a high number of API calls (40 per minute for demo accounts). To prevent exceeding the API limits, stock data will be stored in .txt files, with a limit of 10 stocks per file.

## Features

### 1. Opportunity Analysis
This section allows you to run simple technical indicators against predetermined stock symbols to assess investment opportunities.

- **Timeframes**:
    - 1 Hour
    - 8 Hours
    - 1 Day

- **Indicators**:
    - **RSI (Relative Strength Index)**: 
        - Over 70 → Overbought (Sell)
        - Under 30 → Oversold (Buy)
    - **MACD (Moving Average Convergence Divergence)**:
        - MACD line crosses below the Signal Line → Price is falling (Sell)
        - MACD line crosses above the Signal Line → Price is rising (Buy)
    - **ADX (Average Directional Index)**:
        - ADX above 40 and DI- above DI+ → Price is falling (Sell)
        - ADX above 40 and DI+ above DI- → Price is rising (Buy)

### Stock Symbol Lists
The stock symbols will be grouped into lists stored in `.txt` files (So i give a page to client so he can create stock lists on website). These lists will contain a maximum of 10 stocks each. You will be able to create multiple stock lists, such as:

- **USA Stocks**
- **UK Stocks**
- **Current Portfolio**

These lists will be accessible via a dropdown list on the website.

### Indicators and Results Table
The website will generate results for each stock, showing how each indicator has performed. The results will be displayed in a table format, which will include:

| **Stock** | **RSI**         | **MCAD**     | **ADI**        | **Results** |
|-----------|-----------------|--------------|----------------|-------------|
| AAPL      | N/A - [value]    | BUY          | N/A            | 1           |
| TSLA      | BUY - [value]    | BUY          | BUY            | 3           |
| MSFT      | N/A - [value]    | BUY          | BUY            | 2           |
| ZM        | SELL - [value]   | SELL         | SELL           | 3           |
| GE        | BUY - [value]    | BUY          | N/A            | 2           |

- **N/A**: Indicates that the RSI value is between 30 and 70 or the ADX value is below 40.
- **Results**: The number of indicators that give the same outcome (Buy/Sell).
  ## Technologies Used

## Technologies Used

- **Flask**: Web framework for building the website.
- *Tailwind CSS**: Utility-first CSS framework for designing responsive and customizable user interfaces.
- **Alpaca API**: For stock analysis and trading data.
- **NGINX**: Web server used to reverse proxy the Flask application.
- **Gunicorn**: WSGI HTTP server for running the Flask app in production.
- **GitHub**: For version control and collaboration on the project.
- **Git**: Distributed version control system for managing code.
- **AWS EC2**: For hosting the website on the cloud.


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2.Create a virtual environment:
 ```bash
   python -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate     # For Windows
  ```
Install dependencies:
```bash
 pip install -r requirements.txt
  ```
Run the Flask application:
```bash
python run.py
  ```
Your development server will start, and you can view the application
locally at http://127.0.0.1:5000/.
#To use taiwlind in the project stylinf
1.Install dependencies through 
```bash
npm install
```
After making hcages in css and adding classws to generate the css 
```bash
npx tailwindcss -i app/static/css/input.css -o app/static/css/tailwind.css
```
This will generate css in static css tailwind.css file


