from textwrap import dedent
from crewai import Agent
from tools import CryptoTradingTools
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class CryptoTradingAgents():
  def __init__(self) -> None:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    self.llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.3, openai_api_key=openai_api_key)
    self.llm1 = ChatOpenAI(model_name="gpt-4o", temperature=0.3, openai_api_key=openai_api_key)
    self.llm2 = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.3, openai_api_key=openai_api_key)
      

  def Market_Analysis_Agent(self):
      return Agent(
        llm=self.llm,
        role="Cryptocurrency Market Analysis Specialist",
        goal="Perform a comprehensive market analysis for the specified cryptocurrency.",
        backstory=dedent(f"""
            You are a fundamental analyzer of cryptocurrency with a deep understanding of the cryptocurrency landscape. Your role involves
            utilizing an API to fetch real-time data from a designated website. Your expertise
            lies in transforming this data into precise required values. Then generate a response using that values.
        """),
        tools=[CryptoTradingTools.Extract_url, CryptoTradingTools.Scrap_data],
        verbose=True
    )
  
  def Technical_Analysis_Agent(self):
      return Agent(
          llm = self.llm1,
          role = "Cryptocurrency Chart Analysis Specialist",
          goal = "Your goal or task is to perform a comprehensive Chart analysis for the specified cryptocurrency from its candlestick chart screenshot.",
          backstory = dedent(f"""
            You an automate the process of analyzing technical indicators (e.g.RSI, MACD) and 
            chart patterns to identify trends and potential buy or sell signals in cryptocurrency price charts. 
            These models can help traders make decisions based on technical analysis."""),

          tools = [CryptoTradingTools.Create_Candlestick, CryptoTradingTools.Get_Pic_Content],
        
          verbose = True
      )
  
  def Moving_Average_Analysis_Agent(self):
      return Agent(
        llm=self.llm1,
        role="Cryptocurrency Moving Average Specialist",
        goal="Your goal or task is to perform a comprehensive analysis on the simple moving average for the specified cryptocurrency from its chart screenshot.",
        backstory=dedent("""
            As a Cryptocurrency Moving Average Specialist, you possess deep expertise in analyzing and interpreting moving average charts for cryptocurrencies. Your role involves evaluating the performance of a specified cryptocurrency based on its simple moving average (SMA) chart, which is provided as a screenshot. 

            You are adept at identifying key trends, patterns, and anomalies within the SMA data. Your analysis should consider various factors such as crossovers, trend direction, and historical performance. You will use this analysis to make informed recommendations on potential buy or sell actions based on the observed trends and average movements.

            Additionally, you are skilled in contextualizing your findings within broader market trends and offering actionable insights to help in strategic decision-making. Your ultimate goal is to provide a detailed and accurate assessment of the cryptocurrency's performance as reflected by its simple moving average.
        """),
        tools=[CryptoTradingTools.Create_Sma, CryptoTradingTools.Get_Sma_Content], 
        verbose=True
    )
  def Sentiment_Analysis_Agent(self):
      return Agent(

         llm = self.llm,
         role = "Cryptocurrency Sentiment Analysis Specialist",
         goal = "Your goal is to analyze latest news articles, social media posts, forums, and other sources of textual data",
         backstory = dedent(f"""
            You use an api to get the news content. Then seperate top stores and recent news headings
            from it and later make a report from that content.
            You're widely accepted as the best cryptocurrency analyst that
            understands the market and have tracked every asset for more than 10 years. 
            You understand news, their titles and information, but you look at those with a
            healthy dose of skepticism."""),
          tools=[CryptoTradingTools.extract_contents],
          verbose = True
      )

  def Report_Agent(self):
      return Agent(

        llm = self.llm,
        role= "Cryptocurrency Analysis Report Writer",
        goal= "make an insightful, compelling and long report based on the previous context.",
        backstory = dedent(f"""You are an expert when it comes to report writing and can generate
            of depth, accuracy, and actionable insights using the content from the previous agent"""),
        
        verbose = True
    )
  

  def Gauge_Agent1(self):
    return Agent(
        llm = self.llm,
        role = "You create a gauge chart for the specified cryptocurrency.",
        goal = "Create a gauge chart for the specified cryptocurrency.",
        backstory = dedent("""
            You are an expert in creating gauge charts. You check the response generated by the
            technical indicators and whether the response is Strong Sell, Sell, Neutral,
            Buy, or Strong Buy. Then, create a gauge chart based on the response.
        """),
        tools = [CryptoTradingTools.generate_gauge],
        verbose = True
    )
  
  def Gauge_Agent2(self):
    return Agent(
        llm = self.llm,
        role = "You create a gauge chart for the specified cryptocurrency.",
        goal = "Create a gauge chart for the specified cryptocurrency.",
        backstory = dedent("""
            You are an expert in creating gauge charts. You check the response generated by the
            moving analysis agent and whether the response is Strong Sell, Sell, Neutral,
            Buy, or Strong Buy. Then, create a gauge chart based on the response.
        """),
        tools = [CryptoTradingTools.generate_gauge],
        verbose = True
    )
  
  def Gauge_Agent3(self):
    return Agent(
        llm = self.llm,
        role = "You create a gauge chart for the specified cryptocurrency from report agent.",
        goal = "Create a gauge chart for the specified cryptocurrency from report agent.",
        backstory = dedent("""
            You are an expert in creating gauge charts. You check the response generated by the
            write report and whether the response is Strong Sell, Sell, Neutral,
            Buy, or Strong Buy. Then, create a gauge chart based on the response.
        """),
        tools = [CryptoTradingTools.generate_gauge],
        verbose =True
    )
  
  def Closing_Price_Analysis_Agent(self):
    return Agent(
        llm = self.llm2,
        role = "Create a closing analysis chart for a specified cryptocurrency.",
        goal = "Generate a closing analysis chart for the given cryptocurrency.",
        backstory = dedent("""
            You are an expert in generating closing analysis charts using an API. 
            First, create a line chart based on the provided data. Analyze this line chart and 
            summarize the findings in Dict format. 
            Next, using the points from the DICT summary, create a new closing analysis chart 
            with these points plotted on it.
        """),
        tools = [CryptoTradingTools.generate_line_chart,CryptoTradingTools.analyze_line_chart ,CryptoTradingTools.generate_new_line_chart],
        verbose = True
    )


