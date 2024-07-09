from textwrap import dedent
from crewai import Task

class CryptoTradingTasks():
  def Perform_Market_Analysis(self, agent, coin):
    return Task(
            description=dedent(f"""
                Your role involves obtaining a URL using a tool and fetching real-time data from a designated website using another tool.
                Continue this task until you successfully retrieve the content from the website; do not proceed to the next task until this is accomplished.
                Your expertise lies in extracting the following values from the retrieved content and generate a report using these:
                1. Current Price(Live Price) and Percentage Change
                2. Market Capitalization (MARKETCAP)
                3. Circulating Supply
                4. 24-Hour Trading Volume
                5. Total Supply
                6. Initial Token Price
                7. Fully Diluted Valuation
                8. 24-Hour High and Low Prices
                9. All-Time High and Low Prices
                Print these values after extracting them. Ensure accuracy; the values will be provided in the website's content.
                Coin: {coin}
            """),
            expected_output=dedent(f"""
               Make a report using these values and if something important is also extracted then include it too in the report.
                                   

            """),
            agent=agent
        )
  

  def Perform_Chart_Analysis(self, agent, coin):
      return Task(
          description= dedent(f"""
              Your role involves extracting a symbol and then take a screenshot of the candlestick chart 
              from a given website using a tool. You analyze candlestick charts to understand market sentiment 
              and price movements. By interpreting the patterns formed by candlesticks, they can make informed predictions 
              about future price directions. You assess the overall trend of the market (uptrend, downtrend,
              or sideways) by analyzing the candlestick patterns over various time frames. You can also detect 
              crucial support and resistance levels by analyzing where prices have historically reversed or stalled.
              You can generate buy or sell signals based on predefined criteria and candlestick patterns.
                              
              Coin: {coin}
          """),
          expected_output = dedent(f"""
                                   
          1. Trend Analysis:
                - Identify the current trend (uptrend, downtrend, or sideways).
                - Determine trend strength and potential reversal points.
            
            2. Support and Resistance Levels:
                - Identify major support and resistance levels.
                - Highlight any significant breakouts or breakdowns.
            
            3. Candlestick Patterns:
                - Detect and interpret common candlestick patterns (e.g., Doji, Hammer, Engulfing patterns, Harami etc).
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

            
          Generate a comprehensive report from the analysis which includes:
          - Identification of the overall market trend (uptrend, downtrend, or sideways) across different time frames.
          - Key candlestick patterns detected and their interpretations.
          - Crucial support and resistance levels identified based on historical price reversals or stalls.
          - Buy or sell signals generated based on predefined criteria and candlestick patterns.
          - A summary of the potential future price directions with rationale.
          """),
          agent = agent
        )


  def Get_News(self, agent, coin):
       return Task(
        description=dedent(f"""
        Using the provided coin ({coin}), utilize the search tool to find recent websites(blogs) and news related to it. 
        Then Extract the relevant content from these sources.
        Using the list of urls of trending websites provided, your task is to extract relevant content related to the topic '{coin}'.
        Focus on extracting comprehensive and relevant information that can be used to create a comprehensive and helpful report.
        Ensure that the extracted content is organized, cleaned, and formatted appropriately for further processing.

        Compose the extracted content into a comprehensive and helpful report.
        """),

        expected_output=dedent(f"""
            The expected output is a well-researched and engaging report from the extracted content of the websites.
        """),

        agent=agent

    )


  def Write_Rport(self, agent):
      return Task(
         
         description = dedent(f"""
            Use the previous context to create a detailed report. You should tell the user how to approach to buy
            that coin based on the analysis you have done from the content The report should include:
                1. Market Analysis
                2. Chart Analysis
                3. Sentiment Analysis
                These three will be copied from the previous context and the next analysis you will provide will be the examination of these three:
                4. Your Analysis
            """),
        
        expected_output=dedent(f"""
            The expected output is a comprehensive report of atleast 4 pages that includes the following sections:
                1. Market Analysis
                2. Chart Analysis
                3. Sentiment Analysis
                4. Your Analysis
            """),
        
        agent=agent,

      )
  
