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
                6. Fully Diluted Valuation
                7. 24-Hour High and Low Prices
                8. All-Time High and Low Prices
                Print these values after extracting them. Ensure accuracy; the values will be provided in the website's content.
                Coin: {coin}
            """),
            expected_output=dedent(f"""
               Make a report using these values.
               Also tell about if the asset is undervalued or overvalued:
    
                                   

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
        Using the provided coin ({coin}), extract the contents of the website using the urls already provided.
        your task is to extract relevant content related to the topic '{coin}'.
        After extracting format the content where it contains the top stories and the latest news that happened.
        Ensure that the extracted content is organized, cleaned, and formatted appropriately for further processing.

        """),
        expected_output = dedent("""
          First mention the list of top stories of the coin plus the latest stories too.
          - Top Stories
          - Latest Stories
                                 
          Then generate the report of the following sections:

          1. Summary of Content: Provide a summary of the key points from the extracted content.

          2. Sentiment Analysis: Evaluate the overall sentiment of the news articles. Indicate whether the sentiment is neutral, negative, or positive.

          3. Key Insights: Highlight any significant trends, insights, or notable information from the content.

          Make sure your report is clear, concise, and organized. Provide specific examples or quotes from the content to support your analysis.
      """),
        agent=agent
    )


  def Write_Rport(self, agent):
      return Task(
         
         description = dedent(f"""
            Use the previous context to create a detailed report. You should tell the user how to approach to buy
            that coin based on the analysis you have done from the content The report should include:
                1. Market Analysis (summary)
                2. Chart Analysis (summary)
                3. Sentiment Analysis (summary)
                These three will be copied from the previous context and the next analysis you will provide will be your overview
                on whether to buy this coin or sell it and give the reason behind your answer. Answer from the context of the previous analyses.
                Give a detailed analysis so that the user can feel confident what to decision to take.
                4. AI Analysis
            """),
        
        expected_output=dedent(f"""
            The expected output is a comprehensive report of atleast 4 pages that includes the following sections:
                1. Market Analysis (summary)
                2. Chart Analysis (summary)
                3. Sentiment Analysis (summary)
                4. Your Analysis (detailed)
            """),
        
        agent=agent,

      )
  
