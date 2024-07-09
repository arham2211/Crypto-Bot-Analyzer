from crewai import Crew
import streamlit as st
from fpdf import FPDF
from agents import CryptoTradingAgents
from tasks import CryptoTradingTasks



# class CryptoTradingAgents():
#   def __init__(self) -> None:
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     google_api_key = os.getenv("GOOGLE_API_KEY")
#     self.llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.3, openai_api_key=openai_api_key)
#     self.llm1 = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=google_api_key)
      


#   def Market_Analysis_Agent(self):
#       return Agent(
#         llm=self.llm,
#         role="Cryptocurrency Market Analysis Specialist",
#         goal="Perform a comprehensive market analysis for the specified cryptocurrency.",
#         backstory=dedent(f"""
#             You are an experienced market analyst with a deep understanding of the cryptocurrency landscape. Your role involves
#             utilizing an API to fetch real-time data from a designated website. Your expertise
#             lies in transforming this data into precise required values. Then generate a response using that values.
#         """),
#         tools=[CryptoTradingTools.Extract_url, CryptoTradingTools.Scrap_data],
#         verbose=True
#     )
  
#   def Technical_Analysis_Agent(self):
#       return Agent(
#           llm = self.llm1,
#           role = "Cryptocurrency Chart Analysis Specialist",
#           goal = "Your goal or task is to perform a comprehensive Chart analysis for the specified cryptocurrency from its candlestick chart screenshot.",
#           backstory = dedent(f"""
#             You an automate the process of analyzing technical indicators (e.g., moving averages, RSI, MACD) and 
#             chart patterns to identify trends and potential buy or sell signals in cryptocurrency price charts. 
#             These models can help traders make decisions based on technical analysis."""),

#           tools = [CryptoTradingTools.Take_ss, CryptoTradingTools.Get_Pic_Content],
        
#           verbose = True
#       )

#   def Sentiment_Analysis_Agent(self):
#       return Agent(
         
#          llm = self.llm,
#          role = "Cryptocurrency Sentiment Analysis Specialist",
#          goal = "Your goal is to analyze news articles, social media posts, forums, and other sources of textual data",
#          backstory = dedent(f"""
#             You get URLS of articles, websites, news and extract their content and later make a report from 
#             that content.
#             You're widely accepted as the best cryptocurrency analyst that
#             understands the market and have tracked every asset for more than 10 years. 
#             You understand news, their titles and information, but you look at those with a
#             healthy dose of skepticism."""),

#           tools = CryptoTradingTools.tools(),
#           verbose = True
#       )

#   def Report_Agent(self):
#       return Agent(

#         llm = self.llm,
#         role= "Cryptocurrency Analysis Report Writer",
#         goal= "make an insightful, compelling and long report based on the previous context.",
#         backstory = dedent(f"""You are an expert when it comes to report writing and can generate
#             of depth, accuracy, and actionable insights using the content from the previous agent"""),
        
#         verbose = True
#     )

# class CryptoTradingTasks():
#   def Perform_Market_Analysis(self, agent, coin):
#     return Task(
#             description=dedent(f"""
#                 Your role involves obtaining a URL using a tool and fetching real-time data from a designated website using another tool.
#                 Continue this task until you successfully retrieve the content from the website; do not proceed to the next task until this is accomplished.
#                 Your expertise lies in extracting the following values from the retrieved content and generate a report using these:
#                 1. Current Price(Live Price) and Percentage Change
#                 2. Market Capitalization (MARKETCAP)
#                 3. Circulating Supply
#                 4. 24-Hour Trading Volume
#                 5. Total Supply
#                 6. Initial Token Price
#                 7. Fully Diluted Valuation
#                 8. 24-Hour High and Low Prices
#                 9. All-Time High and Low Prices
#                 Print these values after extracting them. Ensure accuracy; the values will be provided in the website's content.
#                 Coin: {coin}
#             """),
#             expected_output=dedent(f"""
#                Make a report using these values and if something important is also extracted then include it too in the report.
                                   

#             """),
#             agent=agent
#         )
  

#   def Perform_Chart_Analysis(self, agent, coin):
#       return Task(
#           description= dedent(f"""
#               Your role involves extracting a symbol and then take a screenshot of the candlestick chart 
#               from a given website using a tool. You analyze candlestick charts to understand market sentiment 
#               and price movements. By interpreting the patterns formed by candlesticks, they can make informed predictions 
#               about future price directions. You assess the overall trend of the market (uptrend, downtrend,
#               or sideways) by analyzing the candlestick patterns over various time frames. You can also detect 
#               crucial support and resistance levels by analyzing where prices have historically reversed or stalled.
#               You can generate buy or sell signals based on predefined criteria and candlestick patterns.
                              
#               Coin: {coin}
#           """),
#           expected_output = dedent(f"""
                                   
#           1. Trend Analysis:
#                 - Identify the current trend (uptrend, downtrend, or sideways).
#                 - Determine trend strength and potential reversal points.
            
#             2. Support and Resistance Levels:
#                 - Identify major support and resistance levels.
#                 - Highlight any significant breakouts or breakdowns.
            
#             3. Candlestick Patterns:
#                 - Detect and interpret common candlestick patterns (e.g., Doji, Hammer, Engulfing patterns, Harami etc).
#                 - Provide insights on potential bullish or bearish signals based on these patterns.
            
#             4. Moving Averages:
#                 - Calculate and analyze moving averages (e.g., 50-day, 200-day).
#                 - Identify any crossovers (e.g., Golden Cross, Death Cross) and their implications.
            
#             5. Volume Analysis:
#                 - Analyze volume trends to confirm price movements.
#                 - Highlight any unusual volume spikes and their potential impact.

#             6. Risk Assessment:
#                 - Assess potential risks and provide suggestions for risk management (e.g., stop-loss levels).

#             7. Summary and Recommendations:
#                 - Summarize key findings from the analysis.
#                 - Provide actionable trading recommendations based on the analysis.

            
#           Generate a comprehensive report from the analysis which includes:
#           - Identification of the overall market trend (uptrend, downtrend, or sideways) across different time frames.
#           - Key candlestick patterns detected and their interpretations.
#           - Crucial support and resistance levels identified based on historical price reversals or stalls.
#           - Buy or sell signals generated based on predefined criteria and candlestick patterns.
#           - A summary of the potential future price directions with rationale.
#           """),
#           agent = agent
#         )


#   def Get_News(self, agent, coin):
#        return Task(
#         description=dedent(f"""
#         Using the provided coin ({coin}), utilize the search tool to find recent websites(blogs) and news related to it. 
#         Then Extract the relevant content from these sources.
#         Using the list of urls of trending websites provided, your task is to extract relevant content related to the topic '{coin}'.
#         Focus on extracting comprehensive and relevant information that can be used to create a comprehensive and helpful report.
#         Ensure that the extracted content is organized, cleaned, and formatted appropriately for further processing.

#         Compose the extracted content into a comprehensive and helpful report.
#         """),

#         expected_output=dedent(f"""
#             The expected output is a well-researched and engaging report from the extracted content of the websites.
#         """),

#         agent=agent

#     )


#   def Write_Rport(self, agent):
#       return Task(
         
#          description = dedent(f"""
#             Use the previous context to create a detailed report. You should tell the user how to approach to buy
#             that coin based on the analysis you have done from the content The report should include:
#                 1. Market Analysis
#                 2. Chart Analysis
#                 3. Sentiment Analysis
#                 These three will be copied from the previous context and the next analysis you will provide will be the examination of these three:
#                 4. Your Analysis
#             """),
        
#         expected_output=dedent(f"""
#             The expected output is a comprehensive report of atleast 4 pages that includes the following sections:
#                 1. Market Analysis
#                 2. Chart Analysis
#                 3. Sentiment Analysis
#                 4. Your Analysis
#             """),
        
#         agent=agent,

#       )
  

# class CryptoTradingTools():

#   @tool("Extract URL")
#   def Extract_url(coin_name :str):
#     """Extract the url of the website."""
#     tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
#     url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

#     headers = {
#         "accept": "application/json",
#         "api_key": tokenmetrics_api_key
#     }
#     if coin_name.lower() == "bnb":
#         return f"https://coinmarketcap.com/currencies/{coin_name}/"

#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#       data = response.json()
#       if data["success"]:
#         for coin in data["data"]:
#           if coin["TOKEN_NAME"].lower() == coin_name.lower():
#             part = coin['TM_LINK']
#             parsed_url = urlparse(part)
#             path = parsed_url.path
#             last_word = path.split('/')[-1]
#             return f"https://coinmarketcap.com/currencies/{last_word}/"

                    
#       else:
#         return "Failed to fetch data. API response indicates failure."
#     else:
#       return f"Failed to fetch data. Status code: {response.status_code}"

#   @tool("Scrap data from the Website")
#   def Scrap_data(url: str):
#     """Scrap data from the Website and print it."""

#     loader = WebBaseLoader(url)
#     data = loader.load()
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
#     splits = splitter.split_documents(data)

#     return splits
    
#   @tool("Extract symbol and take screenshot from the website provided")
#   def Take_ss(coin_name: str):
#     """Extract symbol and Take screen shot from the website""" 
#     tokenmetrics_api_key = os.getenv('TOKENMETRICS_API_KEY')
#     url = "https://api.tokenmetrics.com/v2/tokens?category=yield%20farming%2Cdefi&exchange=binance%2Cgate&blockchain_address=binance-smart-chain%3A0x57185189118c7e786cafd5c71f35b16012fa95ad&limit=10000&page=0"

#     headers = {
#         "accept": "application/json",
#         "api_key": tokenmetrics_api_key
#     }

#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#       data = response.json()
#       if data["success"]:
#         for coin in data["data"]:
#           if coin["TOKEN_NAME"].lower() == coin_name.lower():
#             token = coin["TOKEN_SYMBOL"]     
        
#         options = Options()
#         options.headless = True
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#         try:
#           driver.maximize_window()
#           driver.get(f"https://www.binance.com/en/trade/{token}_USDT?_from=markets&type=spot")
#           time.sleep(10)  # Wait for the page to load
#           arrow_down_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-1mfpw7s"]')))
    
#           # Create action chain object
#           actions = ActionChains(driver)
            
#           # Perform hover action
#           actions.move_to_element(arrow_down_button).perform()
            

#           # Find and click the button for the 1-month view
#           one_month_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-bn-type="text" and text()="1M"]')))
#           one_month_button.click()
        
#           # Wait for the chart to update
#           time.sleep(5)  # Adjust this based on how long it takes for the chart to update

#           driver.save_screenshot("coin_screenshot.png")
#           print("Screenshot taken successfully.")
#         finally:
#           driver.quit()

#   @tool("Extract the content from the image")
#   def Get_Pic_Content():
#     "Extract the content from the image"
#     genai.configure(api_key="AIzaSyAflO1ApOXZCQsmJo4YSN8ZMhyyas11oEQ")

#     model = genai.GenerativeModel('gemini-pro-vision')

#     image_path = "coin_screenshot.png"  

#     try:
#         with open(image_path, "rb") as image_file:
#             bytes_data = image_file.read()
#     except FileNotFoundError:
#         return "Image file not found."
#     except Exception as e:
#         return f"An error occurred while reading the image file: {e}"

#     mime_type, _ = mimetypes.guess_type(image_path)
#     if not mime_type:
#         return "Unable to determine the MIME type of the image."

#     image_parts = [
#         {
#             "mime_type": mime_type,
#             "data": bytes_data
#         }
#     ]

#     input_prompt = """        
#             Perform a comprehensive technical analysis of the provided candlestick chart to identify key market trends, patterns, and potential trading signals.

#             1. Trend Analysis:
#                 - Identify the current trend (uptrend, downtrend, or sideways).
#                 - Determine trend strength and potential reversal points.
            
#             2. Support and Resistance Levels:
#                 - Identify major support and resistance levels.
#                 - Highlight any significant breakouts or breakdowns.
            
#             3. Candlestick Patterns:
#                 - Detect and interpret common candlestick patterns (e.g., Doji, Hammer, Engulfing patterns, etc).
#                 - Provide insights on potential bullish or bearish signals based on these patterns.
            
#             4. Moving Averages:
#                 - Calculate and analyze moving averages (e.g., 50-day, 200-day).
#                 - Identify any crossovers (e.g., Golden Cross, Death Cross) and their implications.
            
#             5. Volume Analysis:
#                 - Analyze volume trends to confirm price movements.
#                 - Highlight any unusual volume spikes and their potential impact.

#             6. Risk Assessment:
#                 - Assess potential risks and provide suggestions for risk management (e.g., stop-loss levels).

#             7. Summary and Recommendations:
#                 - Summarize key findings from the analysis.
#                 - Provide actionable trading recommendations based on the analysis.

#             Print all these outputs line by line with headings."""

#     try:
#         response = model.generate_content([input_prompt, image_parts[0]])
#     except Exception as e:
#         return f"An error occurred while generating content: {e}"

#     return response.text

#   @tool
#   def search(query: str):
#     """Search for a webpage based on the query."""
#     return CryptoTradingTools._exa().search(f"{query}", use_autoprompt=True, num_results=2)
  
#   @tool
#   def find_similar(url: str):
#       """Search for webpages or articles similar to a given URL.
#       The url passed in should be a URL returned from `search`.
#       """
#       return CryptoTradingTools._exa().find_similar(url, num_results=2)

#   @tool
#   def get_contents(urls: str):
#       """Get the contents of a webpage.
#       """
#       content = []
#       for url in urls:
#         loader = WebBaseLoader(url)
#         data = loader.load()
#         content.append(data)
      
#       return content
         
#     #   ids = eval(ids)

#     #   contents = str(CryptoTradingTools._exa().get_contents(ids))
#     #   contents = contents.split("URL:")
#     #   contents = [content[:1000] for content in contents]
#     #   return "\n\n".join(contents)
    
#   def tools():
#     return [
#       CryptoTradingTools.search,
#       CryptoTradingTools.find_similar,
#       CryptoTradingTools.get_contents
#     ]


#   def _exa():
#     api_key = os.getenv('EXA_API_KEY')
#     return Exa(api_key=api_key)


def main():
    st.title("Cryptocurrency Analysis Report")

    coin_name = st.text_input("Enter the coin name:")
    if st.button("Run Analysis"):
        agents = CryptoTradingAgents()
        tasks = CryptoTradingTasks()

        Market_Analysis_Agent = agents.Market_Analysis_Agent()
        Technical_Analysis_Agent = agents.Technical_Analysis_Agent()
        Sentiment_Analysis_Agent = agents.Sentiment_Analysis_Agent()
        Report_Agent = agents.Report_Agent()

        Perform_Market_Analysis = tasks.Perform_Market_Analysis(Market_Analysis_Agent, coin_name)
        Perform_Chart_Analysis = tasks.Perform_Chart_Analysis(Technical_Analysis_Agent, coin_name)
        Get_News = tasks.Get_News(Sentiment_Analysis_Agent, coin_name)
        Write_Rport = tasks.Write_Rport(Report_Agent)

        Write_Rport.context = [Perform_Market_Analysis, Perform_Chart_Analysis, Get_News]

        crew1 = Crew(
     
        agents=[Market_Analysis_Agent],
        tasks=[Perform_Market_Analysis],
        verbose=True

        )
  
        result1 = crew1.kickoff()
        st.subheader("Market Analysis Results")
        st.write(result1)
        
        crew2 = Crew(
            
            agents=[Technical_Analysis_Agent],
            tasks=[Perform_Chart_Analysis],
            verbose=True

            )
        
        result2 = crew2.kickoff()
        st.subheader("Technical Analysis Results")
        st.write(result2)
        
        crew3 = Crew(
            
            agents=[Sentiment_Analysis_Agent],
            tasks=[Get_News],
            verbose=True

            )

        result3 = crew3.kickoff()
        st.subheader("Sentiment Analysis Results")
        st.write(result3)


        crew4 = Crew(
            
            agents=[Report_Agent],
            tasks=[Write_Rport],
            verbose=True

            )

        result4 = crew4.kickoff()

        st.subheader("Final Report")
        st.write(result4)

        # Save results to PDF
        pdf_file = save_to_pdf(result1, result2, result3, result4)
        st.success(f"Results saved to {pdf_file}")

        # Add download button
        st.download_button(
            label="Download PDF",
            data=open(pdf_file, "rb").read(),
            file_name=pdf_file,
            mime="application/pdf",
        )

def save_to_pdf(result1, result2, result3, result4):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, "Market Analysis Results:\n" + str(result1))
    pdf.add_page()
    pdf.multi_cell(0, 10, "Technical Analysis Results:\n" + str(result2))
    pdf.add_page()
    pdf.multi_cell(0, 10, "Sentiment Analysis Results:\n" + str(result3))
    pdf.add_page()
    pdf.multi_cell(0, 10, "Final Report:\n" + str(result4))

    pdf_file = "analysis_results.pdf"
    pdf.output(pdf_file)
    return pdf_file



if __name__ == "__main__":
    main()
