import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from langchain_community.document_loaders import WebBaseLoader
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.parse import urlparse
from langchain.agents import tool
from exa_py import Exa
from openai import OpenAI
import base64
import time
import os

 


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
    
  @tool("Extract symbol and take screenshot from the website provided")
  def Take_ss(coin_name: str):
    """Extract symbol and Take screen shot from the website""" 
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
        
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
          driver.maximize_window()
          driver.get(f"https://www.binance.com/en/trade/{token}_USDT?_from=markets&type=spot")
          time.sleep(10)  # Wait for the page to load
          arrow_down_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-1mfpw7s"]')))
    
          # Create action chain object
          actions = ActionChains(driver)
            
          # Perform hover action
          actions.move_to_element(arrow_down_button).perform()
            

          # Find and click the button for the 1-month view
          one_month_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-bn-type="text" and text()="1M"]')))
          one_month_button.click()
        
          # Wait for the chart to update
          time.sleep(5)  # Adjust this based on how long it takes for the chart to update

          driver.save_screenshot("coin_screenshot.jpeg")
          print("Screenshot taken successfully.")
        finally:
          driver.quit()

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

### 4. Moving Averages
**Calculate and Analyze Moving Averages**:
- **50-Day Moving Average (SMA)**
- **200-Day Moving Average (SMA)**

**Identify Any Crossovers**:
- **Golden Cross**: Short-term MA crosses above long-term MA, indicating potential bullish trend.
- **Death Cross**: Short-term MA crosses below long-term MA, indicating potential bearish trend.

### 5. Volume Analysis
**Analyze Volume Trends**:
- Confirm price movements with corresponding volume. An increase in volume confirms the strength of the price movement.

**Unusual Volume Spikes**:
- Identify significant volume spikes which can indicate strong buying/selling pressure and potential trend changes.

### 6. Risk Assessment
**Potential Risks and Suggestions for Risk Management**:
- Identify levels for stop-loss orders to manage downside risk.
- Suggest appropriate position sizing based on volatility and risk tolerance.


### 7. Summary and Recommendations
**Key Findings**:
- Summarize the identified trend, key support and resistance levels, significant candlestick patterns, and volume analysis.

**Actionable Trading Recommendations**:
- Provide specific recommendations based on the analysis, such as:
  - Buy or sell signals based on trend and pattern analysis.
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

  @tool("Extract the content from the URLS using coin_name")
  def extract_contents(coin_name: str):
    """From the given URLs, extract the contents"""
    loader1 = WebBaseLoader(f"https://crypto.news/tag/{coin_name}/")
    data1 = loader1.load()
    loader2 = WebBaseLoader(f"https://decrypt.co/crypto-news/{coin_name}")
    data2 = loader2.load()
    return data1[0].page_content + data2[0].page_content

  @tool("Fetch top stories")
  def get_top_stories(content: str):
      """Find the top stories and recent news from the content and return a blog of it"""
      new_content = content

      return new_content


  def _exa():
    api_key = os.getenv('EXA_API_KEY')
    return Exa(api_key=api_key)

