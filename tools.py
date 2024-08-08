import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from urllib.parse import urlparse
from langchain.agents import tool
from exa_py import Exa
from openai import OpenAI
import base64
import os
import requests
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import json
 


class CryptoTradingTools():

  @tool("Extract URL")
  def Extract_url(coin_name :str):
    """Extract the url of the website."""
    tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
    url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

    headers = {
        "accept": "application/json",
        "api_key": tokenmetrics_api_key
    }
    if coin_name.lower() == "bnb":
        return f"https://coinmarketcap.com/currencies/{coin_name}/"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if data["success"]:
        for coin in data["data"]:
          if coin["TOKEN_NAME"].lower() == coin_name.lower():
            part = coin['TM_LINK']
            parsed_url = urlparse(part)
            path = parsed_url.path
            last_word = path.split('/')[-1]
            return f"https://coinmarketcap.com/currencies/{last_word}/"

                    
      else:
        return "Failed to fetch data. API response indicates failure."
    else:
      return f"Failed to fetch data. Status code: {response.status_code}"

  @tool("Scrap data from the Website")
  def Scrap_data(url: str):
    """Scrap data from the Website and print it."""

    loader = WebBaseLoader(url)
    data = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(data)

    return splits
    
  @tool("Extract symbol and create candlestick chart from api")
  def Create_Candlestick(coin_name: str):
    """Extract symbol and create candelstick chart from the api""" 
    tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
    url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

    headers = {
        "accept": "application/json",
        "api_key": tokenmetrics_api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if data["success"]:
        for coin in data["data"]:
          if coin["TOKEN_NAME"].lower() == coin_name.lower():
            token = coin["TOKEN_SYMBOL"]

    api_url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{token}USD?apikey=ba164bccb40cdf9d0adc2a9a8cb39060'

    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Extract the historical data
        historical_data = data.get('historical', [])

        # Create a DataFrame from the data
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df.set_index('date', inplace=True)

        # Get the last 30 days of data
        last_30_days_data = df.tail(30)

        # Create a custom style for the candlestick chart
        custom_style = mpf.make_mpf_style(
            base_mpl_style='default',
            rc={'font.size': 8},
            marketcolors=mpf.make_marketcolors(
                up='lime',
                down='red',
                wick={'up':'lime', 'down':'red'},
                volume='skyblue'
            )
        )

        # Create a figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

        # Plot the candlestick chart
        mpf.plot(last_30_days_data, type='candle', style=custom_style, ax=ax1, volume=False)
        ax1.set_title(f'{token}/USD Price', fontsize=16)
        ax1.set_ylabel('Price', fontsize=12)

        # Plot the volume bar chart
        ax2.bar(df.index, df['volume'], width=0.8, align='center', color='skyblue', edgecolor='navy')
        ax2.set_title(f'{token}/USD Trading Volume', fontsize=16)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Volume', fontsize=12)

        # Format x-axis for volume chart
        ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Format y-axis labels for volume chart
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))

        # Add grid lines to volume chart
        ax2.grid(axis='y', linestyle='--', alpha=0.7)

        # Adjust layout and display the plot
        plt.tight_layout()
        plt.savefig('coin_screenshot.jpeg')
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


  @tool("Making small moving average chart")
  def Create_Sma(coin_name: str):
    """Generate the moving average chart then save it"""
    tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
    url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

    headers = {
        "accept": "application/json",
        "api_key": tokenmetrics_api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if data["success"]:
        for coin in data["data"]:
          if coin["TOKEN_NAME"].lower() == coin_name.lower():
            token = coin["TOKEN_SYMBOL"]
    technical_indicator_name = "sma"
    url = f"https://financialmodelingprep.com/api/v3/technical_indicator/1day/{token}USD?type=sma&period=5&apikey=ba164bccb40cdf9d0adc2a9a8cb39060"

    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      df = pd.DataFrame(data)
      df = df[:30]
      df['date'] = pd.to_datetime(df['date'])
      df.set_index('date', inplace=True)

        # Plot the data
      plt.figure(figsize=(14, 7))

      plt.plot(df.index, df['close'], label='Close Price', color='blue')
    
      if technical_indicator_name in df.columns:
        plt.plot(df.index, df[technical_indicator_name], label=f'{technical_indicator_name.upper()} (5)', color='orange')
      else:
        print(f"{technical_indicator_name.upper()} data not available.")
        exit()

      plt.title(f'last 1 month Closing Prices of {token}/USD and {technical_indicator_name.upper()} (5-day)')
      plt.xlabel('Date')
      plt.ylabel('Price (USD)')
      plt.legend()
      plt.grid(True)
      plt.savefig("sma.jpeg")

    else:
        raise Exception(f"Error fetching data: {response.status_code}")

   
  @tool("Extract the content from the image")
  def Get_Sma_Content():
    "Extract the content from the image"
    image_path = "sma.jpeg"  
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    with open(image_path, 'rb') as image_file:
      image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    

    response = client.chat.completions.create(
    model='gpt-4o',
    response_format={"type": "text"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text":
                  """
                  Please analyze the following image of a cryptocurrency moving average chart and provide a detailed summary.
                  The analysis should include:
                  - Key trends and patterns observed in the chart.
                  - Any significant crossovers or anomalies.
                  - An assessment of the current market position based on the chart.
                  - Provide specific recommendations based on the analysis, such as:
                  - Buy or sell signals based on trend and pattern analysis, give one word answer for this from these five options: Strong Sell, Sell, Neutral, Buy, Strong Buy.
                  - Recommendations based on the moving average data.
                        
                  Review the image carefully and provide a comprehensive report.

                  """
                    },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    max_tokens=800,
  )


    return response.choices[0].message.content


  @tool("Extract the content from the image")
  def Get_Pic_Content():
    "Extract the content from the image"
    image_path = "coin_screenshot.jpeg"  
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    with open(image_path, 'rb') as image_file:
      image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    

    response = client.chat.completions.create(
    model='gpt-4o',
    response_format={"type": "text"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text":
                  """
                  To perform a comprehensive technical analysis of a provided candlestick chart and to generate the required outputs, you would typically use specialized software or tools like TradingView, MetaTrader, or similar platforms. Since I don't have access to view or analyze specific images directly, I will provide a detailed framework for how you can conduct this analysis:

                    ### 1. Trend Analysis
                    **Current Trend**:
                    - Identify whether the market is in an uptrend, downtrend, or moving sideways. This can be done by observing the direction of the price movement over time.
                    - **Uptrend**: Higher highs and higher lows.
                    - **Downtrend**: Lower highs and lower lows.
                    - **Sideways**: Horizontal movement with no clear direction.

                    **Trend Strength and Potential Reversal Points**:
                    - Use trend strength indicators like the Average Directional Index (ADX). A high ADX indicates a strong trend.
                    - Look for patterns like Head and Shoulders, Double Tops/Bottoms to identify potential reversal points.

                    ### 2. Support and Resistance Levels
                    **Major Support and Resistance Levels**:
                    - Identify key price levels where the market has repeatedly bounced off (support) or reversed from (resistance).

                    **Significant Breakouts or Breakdowns**:
                    - Highlight any recent price movements that have broken through established support or resistance levels, which may indicate strong future price movement.

                    ### 3. Candlestick Patterns
                    **Common Candlestick Patterns**:
                    - **Doji**: Indicates indecision in the market, potential reversal signal.
                    - **Hammer**: Bullish reversal pattern after a downtrend.
                    - **Engulfing Patterns**: Bullish or bearish, indicating strong reversal potential.

                    **Insights on Potential Bullish or Bearish Signals**:
                    - Bullish patterns suggest potential buying opportunities.
                    - Bearish patterns suggest potential selling opportunities.

                    ### 5. Volume Analysis
                    **Analyze Volume Trends**:
                    - Confirm price movements with corresponding volume. An increase in volume confirms the strength of the price movement.

                    **Unusual Volume Spikes**:
                    - Identify significant volume spikes which can indicate strong buying/selling pressure and potential trend changes.

                    ### 6. Risk Assessment
                    **Potential Risks and Suggestions for Risk Management**:
                    - Identify levels for stop-loss orders to manage downside risk.
                    - Suggest appropriate position sizing based on volatility and risk tolerance.

                    Explain these words too given below
                    - support_price:
                    - consolidation_points_price:
                    - major_resistance_price:
                    - psychological_break_price:
                    - immediate_resistance:   


                    ### 7. Summary and Recommendations
                    **Key Findings**:
                    - Summarize the identified trend, key support and resistance levels, significant candlestick patterns, and volume analysis.

                    **Actionable Trading Recommendations**:
                    - Provide specific recommendations based on the analysis, such as:
                      - Buy or sell signals based on trend and pattern analysis, give one word answer for this from these five options: Strong Sell, Sell, Neutral, Buy, Strong Buy.
                      - Suggested entry and exit points.
                      - Risk management strategies like stop-loss levels.

                  By following this framework, you can systematically analyze a candlestick chart and derive actionable insights for trading decisions.
                  """
                    },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    max_tokens=800,
)


    return response.choices[0].message.content

  @tool("Extract the symbol and extract the data using api")
  def extract_contents(coin_name: str):
    """Extract the symbol and extract the data using api"""

    tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
    url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

    headers = {
        "accept": "application/json",
        "api_key": tokenmetrics_api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if data["success"]:
        for coin in data["data"]:
          if coin["TOKEN_NAME"].lower() == coin_name.lower():
            token = coin["TOKEN_SYMBOL"]

    url = f"https://financialmodelingprep.com/api/v4/crypto_news?page=1&symbol={token}USD&apikey=ba164bccb40cdf9d0adc2a9a8cb39060"
    response = requests.get(url)

    
    if response.status_code == 200:  
      data = response.json()
      top_items = data[:5]
      combined_list = []
    
      for item in top_items:
        
        title = item.get('title', 'No Title Found')
        text = item.get('text', 'No Text Found')
        
        # Combine title and text into one string
        combined = f"Title: {title}\nText: {text}"
        
        # Append the combined string to the list
        combined_list.append(combined)

      return combined_list
    


    # coin_name = str(coin_name)

    # try:
    #     loader1 = WebBaseLoader(f"https://crypto.news/tag/{coin_name}/")
    #     data1 = loader1.load()
    #     loader2 = WebBaseLoader(f"https://decrypt.co/crypto-news/{coin_name}")
    #     data2 = loader2.load()

    #     content1 = data1[0].page_content if data1 else "No content found at the first URL."
    #     content2 = data2[0].page_content if data2 else "No content found at the second URL."

    #     return content1 + content2
    # except Exception as e:
    #     return f"An error occurred while extracting content: {str(e)}"


  @tool("Create a gauge chart")
  def generate_gauge(context: str):
    """Create a gauge chart from the context or approach received and save it"""
    colors = ['#4dab6d', "#72c66e", "#f6ee54", "#f36d54", "#ee4d55"]
    words = ["strong sell", "sell", "neutral", "buy", "strong buy"]

    context = context.lower()
    value = 0

    for word in words:
        if word in context:
            if word == "strong buy":
                value = 2.85
            elif word == "strong sell":
                value = 0.25
            elif word == "buy":
                value = 2.20
            elif word == "sell":
                value = 0.90
            elif word == "neutral":
                value = 1.55

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection="polar")

    # Adjusting the positions and widths
    x = [0, 0.6, 1.2, 1.9, 2.5]  # Starting positions
    widths = [0.7, 0.7, 0.7, 0.7, 0.65]  # Widths of segments
    
    # Use polar bar plot
    bars = ax.bar(x=x, width=widths, height=0.5, bottom=2,
                  linewidth=3, edgecolor="white",
                  color=colors[::-1], align="edge")  # Reversing color order
    
    # Adjusting text positions and rotations
    plt.annotate("STRONG SELL", xy=(0.2, 2.1), rotation=-70, color="white", fontweight="bold")
    plt.annotate("SELL", xy=(0.89, 2.14), rotation=-40, color="white", fontweight="bold")
    plt.annotate("NEUTRAL", xy=(1.6, 2.2), rotation=0, color="white", fontweight="bold")
    plt.annotate("BUY", xy=(2.3, 2.25), rotation=40, color="white", fontweight="bold")
    plt.annotate("STRONG BUY", xy=(2.9, 2.25), rotation=70, color="white", fontweight="bold")
    
    # Add a needle or indicator
    plt.annotate("", xytext=(0, 0), xy=(value, 2.0),
                 arrowprops=dict(arrowstyle="wedge,tail_width=0.5", color="black", shrinkA=0),
                 bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0),
                 fontsize=45, color="white", ha="center"
                )
    
    plt.title("Performance Gauge Chart", loc="center", pad=20, fontsize=35, fontweight="bold")
    
    # Hide the polar axes
    ax.set_axis_off()
    
    # Adjust layout and save the plot to a file
    plt.tight_layout()
    plt.savefig('gauge.jpeg', dpi=300, bbox_inches='tight')  # Save with high resolution and tight bounding box
    plt.close(fig)  # Close the figure to free up memory
    return "gauge has been created"

    
  @tool("make a line chart and save it")
  def generate_line_chart(coin_name: str):
    """Extract the symbol and create a line chart from the api and save it"""
    tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
    url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

    headers = {
        "accept": "application/json",
        "api_key": tokenmetrics_api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if data["success"]:
        for coin in data["data"]:
          if coin["TOKEN_NAME"].lower() == coin_name.lower():
            token = coin["TOKEN_SYMBOL"]
    
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{token}USD?apikey=ba164bccb40cdf9d0adc2a9a8cb39060"
    response = requests.get(url)
    if response.status_code == 200:
        historical_data = response.json()['historical']
        df_historical = pd.DataFrame(historical_data)
        df_historical['date'] = pd.to_datetime(df_historical['date'])
        df_historical.set_index('date', inplace=True)
        df_historical = df_historical.sort_index()  # Ensure data is sorted by date
        df_historical = df_historical[-30:]
        plt.figure(figsize=(12, 6))
        plt.plot(df_historical.index, df_historical['close'], color='green', linewidth=2)

        # Format the date on the x-axis
        date_form = DateFormatter("%Y-%m-%d")
        plt.gca().xaxis.set_major_formatter(date_form)
        plt.gca().xaxis.set_tick_params(rotation=45)

        # Set plot labels and title
        plt.xlabel('Date')
        plt.ylabel('Closing Price (USD)')
        plt.title(f'{token}/USD Closing Prices (Last 30 Days)')

        # Show plot
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("line_chart.jpeg")
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")

  @tool("analyze the line chart")
  def analyze_line_chart():
     """Analyze the line chart and provide the values in JSON format"""
     image_path = "line_chart.jpeg"  
     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


     with open(image_path, 'rb') as image_file:
      image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    

     response = client.chat.completions.create(
     model='gpt-4o',
     response_format={"type": "text"},
     messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text":
                  """
                  Analyze the line chart of the specified cryptocurrency. The analysis should focus on identifying key price points. The output should be provided in DICT format, 
                  following the structure below:
                  Ouput should be in this format:
                  
                      "support_price": <value>,
                      "consolidation_points_price": <value>,
                      "major_resistance_price": <value>,
                      "psychological_break_price": <value>,
                      "immediate_resistance": <value>
                  
              

        Replace `<value>` with the respective price points identified from the analysis. Ensure that each key is clearly defined and corresponds to the correct price point on the chart.
        
        

                  """
                    },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    max_tokens=800,
  )
     with open('points.txt', 'w') as f:
        f.write(response.choices[0].message.content)
     return response.choices[0].message.content

  
  @tool("Create a new line chart by the values given and save it")
  def generate_new_line_chart(coin_name: str):
    """Create a new line chart by the values and save it"""
    tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
    url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

    headers = {
        "accept": "application/json",
        "api_key": tokenmetrics_api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      if data["success"]:
        for coin in data["data"]:
          if coin["TOKEN_NAME"].lower() == coin_name.lower():
            token = coin["TOKEN_SYMBOL"]

    historical_url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{token}USD?apikey=ba164bccb40cdf9d0adc2a9a8cb39060'
    response = requests.get(historical_url)
    if response.status_code == 200:
        historical_data = response.json()['historical']
        df_historical = pd.DataFrame(historical_data)
        df_historical['date'] = pd.to_datetime(df_historical['date'])
        df_historical.set_index('date', inplace=True)
        df_historical = df_historical.sort_index()
        df_historical = df_historical[-30:]

        with open('points.txt', 'r') as file:
          json_data = file.read()


        data = json.loads(json_data)

          
        support_price = data['support_price']
        consolidation_points_price = data['consolidation_points_price']
        major_resistance_price = data['major_resistance_price']
        psychological_break_price = data['psychological_break_price']
        immediate_resistance = data['immediate_resistance']

        plt.figure(figsize=(12, 6))
        plt.plot(df_historical.index, df_historical['close'], color='green', linewidth=2, label='Closing Price')


        plt.axhline(y=support_price, color='red', linestyle='--', linewidth=1, label='Support Price')
        plt.axhline(y=consolidation_points_price, color='blue', linestyle='--', linewidth=1, label='Consolidation Price')
        plt.axhline(y=major_resistance_price, color='purple', linestyle='--', linewidth=1, label='Major Resistance Price')
        plt.axhline(y=psychological_break_price, color='orange', linestyle='--', linewidth=1, label='Psychological Break Price')
        plt.axhline(y=immediate_resistance, color='brown', linestyle='--', linewidth=1, label='Immediate Resistance Price')


        date_form = DateFormatter("%Y-%m-%d")
        plt.gca().xaxis.set_major_formatter(date_form)
        plt.gca().xaxis.set_tick_params(rotation=45)

        plt.xlabel('Date')
        plt.ylabel('Closing Price (USD)')
        plt.title(f'{token}/USD Closing Prices (Last 30 Days)')


        plt.legend()

        plt.grid(True)
        plt.tight_layout()
        plt.savefig("line_chart.jpeg")
        
        
    else:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")


  def _exa():
    api_key = os.getenv('EXA_API_KEY')
    return Exa(api_key=api_key)

