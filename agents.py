from langchain_google_genai import ChatGoogleGenerativeAI
from textwrap import dedent
from crewai import Agent
from tools import CryptoTradingTools
from langchain_openai import ChatOpenAI
import os


class CryptoTradingAgents():
  def __init__(self) -> None:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # google_api_key = os.getenv("GOOGLE_API_KEY")
    self.llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.3, openai_api_key=openai_api_key)
    self.llm1 = ChatOpenAI(model_name="gpt-4o", temperature=0.3, openai_api_key=openai_api_key)
      

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
            You an automate the process of analyzing technical indicators (e.g., moving averages, RSI, MACD) and 
            chart patterns to identify trends and potential buy or sell signals in cryptocurrency price charts. 
            These models can help traders make decisions based on technical analysis."""),

          tools = [CryptoTradingTools.Take_ss, CryptoTradingTools.Get_Pic_Content],
        
          verbose = True
      )

  def Sentiment_Analysis_Agent(self):
      return Agent(

         llm = self.llm,
         role = "Cryptocurrency Sentiment Analysis Specialist",
         goal = "Your goal is to analyze latest news articles, social media posts, forums, and other sources of textual data",
         backstory = dedent(f"""
            You have 2 URLS from which you extract their contents and then extract ther top stores and recent news headings
            from it and later make a report from that content.
            You're widely accepted as the best cryptocurrency analyst that
            understands the market and have tracked every asset for more than 10 years. 
            You understand news, their titles and information, but you look at those with a
            healthy dose of skepticism."""),
          tools=[CryptoTradingTools.extract_contents, CryptoTradingTools.get_top_stories],
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

