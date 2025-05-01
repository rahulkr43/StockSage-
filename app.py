from flask import Flask, render_template, request
import google.generativeai as genai
import yfinance as yf
import plotly.graph_objects as go
import json

# Configure Google Gemini API
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

class GeminiChat:
    def __init__(self, model="gemini-pro"):
        self.model = genai.GenerativeModel(model)

    def chat(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text if response else "No response received."

# Function to fetch stock price data
def get_stock_data(ticker, period="6mo"):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period)
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

# Function to create an interactive stock price chart
def plot_interactive_stock_data(stock1_data, stock2_data, stock1_name, stock2_name):
    fig = go.Figure()

    # Add Stock 1 prices
    fig.add_trace(go.Scatter(x=stock1_data.index, y=stock1_data["Close"],
                             mode="lines", name=f"{stock1_name}", line=dict(color="blue")))

    # Add Stock 2 prices
    fig.add_trace(go.Scatter(x=stock2_data.index, y=stock2_data["Close"],
                             mode="lines", name=f"{stock2_name}", line=dict(color="red")))

    # Customize layout
    fig.update_layout(title=f"Stock Price Comparison: {stock1_name} vs {stock2_name}",
                      xaxis_title="Date",
                      yaxis_title="Stock Price (USD)",
                      xaxis_rangeslider_visible=True,  # Enables the interactive timeline slider
                      template="plotly_dark")

    # fig.show() # Remove this line, we'll return the figure instead
    return fig  

# Initialize Gemini chatbot
gemini = GeminiChat()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # ... (rest of the Flask app code remains the same)
        # ...

if __name__ == "__main__":
    app.run(debug=True)