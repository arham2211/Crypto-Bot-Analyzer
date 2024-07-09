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
import google.generativeai as genai
from urllib.parse import urlparse
from langchain.agents import tool
from exa_py import Exa
import mimetypes
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

          driver.save_screenshot("coin_screenshot.png")
          print("Screenshot taken successfully.")
        finally:
          driver.quit()

  @tool("Extract the content from the image")
  def Get_Pic_Content():
    "Extract the content from the image"

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro-vision')

    image_path = "coin_screenshot.png"  

    try:
        with open(image_path, "rb") as image_file:
            bytes_data = image_file.read()
    except FileNotFoundError:
        return "Image file not found."
    except Exception as e:
        return f"An error occurred while reading the image file: {e}"

    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        return "Unable to determine the MIME type of the image."

    image_parts = [
        {
            "mime_type": mime_type,
            "data": bytes_data
        }
    ]

    input_prompt = """        
            Perform a comprehensive technical analysis of the provided candlestick chart to identify key market trends, patterns, and potential trading signals.

            1. Trend Analysis:
                - Identify the current trend (uptrend, downtrend, or sideways).
                - Determine trend strength and potential reversal points.
            
            2. Support and Resistance Levels:
                - Identify major support and resistance levels.
                - Highlight any significant breakouts or breakdowns.
            
            3. Candlestick Patterns:
                - Detect and interpret common candlestick patterns (e.g., Doji, Hammer, Engulfing patterns, etc).
                - Provide insights on potential bullish or bearish signals based on these patterns.
            
            4. Moving Averages:
                - Calculate and analyze moving averages (e.g., 50-day, 200-day).
                - Identify any crossovers (e.g., Golden Cross, Death Cross) and their implications.
            
            5. Volume Analysis:
                - Analyze volume trends to confirm price movements.
                - Highlight any unusual volume spikes and their potential impact.

            6. Risk Assessment:
                - Assess potential risks and provide suggestions for risk management (e.g., stop-loss levels).

            7. Summary and Recommendations:
                - Summarize key findings from the analysis.
                - Provide actionable trading recommendations based on the analysis.

            Print all these outputs line by line with headings."""

    try:
        response = model.generate_content([input_prompt, image_parts[0]])
    except Exception as e:
        return f"An error occurred while generating content: {e}"

    return response.text

  @tool
  def search(query: str):
    """Search for a webpage based on the query."""
    return CryptoTradingTools._exa().search(f"{query}", use_autoprompt=True, num_results=2)
  
  @tool
  def find_similar(url: str):
      """Search for webpages or articles similar to a given URL.
      The url passed in should be a URL returned from `search`.
      """
      return CryptoTradingTools._exa().find_similar(url, num_results=2)

  @tool
  def get_contents(urls: str):
      """Get the contents of a webpage.
      """
      content = []
      for url in urls:
        loader = WebBaseLoader(url)
        data = loader.load()
        content.append(data)
      
      return content
         
    #   ids = eval(ids)

    #   contents = str(CryptoTradingTools._exa().get_contents(ids))
    #   contents = contents.split("URL:")
    #   contents = [content[:1000] for content in contents]
    #   return "\n\n".join(contents)
    
  def tools():
    return [
      CryptoTradingTools.search,
      CryptoTradingTools.find_similar,
      CryptoTradingTools.get_contents
    ]


  def _exa():
    api_key = os.getenv('EXA_API_KEY')
    return Exa(api_key=api_key)

