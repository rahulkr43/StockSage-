from flask import Flask, render_template
import google.generativeai as genai
import yfinance as yf
import plotly.graph_objects as go
import json

app = Flask(__name__)

# Configure Google Gemini API
genai.configure(api_key="AIzaSyDFXo6OlB1HVizOPur5MaOQipY**********")  # Replace with your actual API key

class GeminiChat:
    def __init__(self, model="models/chat-bison-001"):  # Replace with a supported model
        self.model = genai.GenerativeModel(model)

    # ... (rest of the code)

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

# Function to create an interactive stock price chart (using Plotly)
def create_interactive_chart(stock1_data, stock2_data, stock1_name, stock2_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock1_data.index, y=stock1_data["Close"],
                             mode="lines", name=f"{stock1_name}", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=stock2_data.index, y=stock2_data["Close"],
                             mode="lines", name=f"{stock2_name}", line=dict(color="red")))
    fig.update_layout(title=f"Stock Price Comparison: {stock1_name} vs {stock2_name}",
                      xaxis_title="Date",
                      yaxis_title="Stock Price (USD)",
                      xaxis_rangeslider_visible=True,
                      template="plotly_dark")
    # Convert the Plotly figure to JSON for rendering in the HTML template
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return chart_json

# Flask route to render the HTML template
@app.route("/")
def index():
    # Get stock data and AI analysis
    stock1 = "NVDA"  # Example stock symbols
    stock2 = "AMD"
    stock1_data = get_stock_data(stock1)
    stock2_data = get_stock_data(stock2)
    gemini = GeminiChat()
    latest_stock1 = stock1_data["Close"].iloc[-1]
    latest_stock2 = stock2_data["Close"].iloc[-1]
    ai_analysis = gemini.chat(f"Compare and analyze the following stock prices:\n- {stock1}: ${latest_stock1:.2f}\n- {stock2}: ${latest_stock2:.2f}")

    # Create interactive chart
    interactive_chart = create_interactive_chart(stock1_data, stock2_data, stock1, stock2)

    # Render the template with the data
    return render_template("index.html", ai_analysis=ai_analysis, interactive_chart=interactive_chart)

if __name__ == "__main__":
    app.run(debug=True)
