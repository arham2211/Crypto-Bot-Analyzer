# Crypto Bot Analyzer Project

This project uses Crew AI to analyze cryptocurrency coin input by the user through three specialized agents and create a comprehensive report based on it analyses. The agents involved are Market_Analysis_Agent, Technical_Analysis_Agent, Sentiment_Analysis_Agent, and Write_Report_Agent. Each agent is tasked with specific functions and uses designated tools to fulfill their roles.

## Agents and Their Tasks

### 1. Market_Analysis_Agent

Analyze the market of the given crypto coin.

**Task:**
- Obtain a URL using the `Extract_url` tool.
- Fetch real-time data from the designated website using the `Scrap_data` tool.
- Generate a report using the fetched content.
  
**Tools:**
- `Extract_url`: Extracts the URL needed for analysis.
- `Scrap_data`: Scrapes real-time data from the extracted URL.

### 2. Technical_Analysis_Agent

Analyze the crypto coin's candlestick chart from Binance.

**Task:**
- Extract a symbol from the provided data.
- Take a screenshot of the candlestick chart from the given Binance website using the `Take_ss` tool.
- Analyze candlestick charts to understand market sentiment and price movements.

**Tools:**
- `Take_ss`: Open Binance Website using selenium and takes a screenshot of the candlestick chart.
- `Get_Pic_Content`: Analyzes the screenshot to extract relevant information.

### 3. Sentiment_Analysis_Agent

Analyze the market of the coin from the news and articles rencently published on it.

**Task:**
- Use the `search` tool to find recent blogs and news websites(articles) related to the given coin name.
- Extract relevant content from these sources using the `find_similar` and `get_contents` tools.

**Tools:**
- `search`: Finds recent websites and blogs.
- `find_similar`: Identifies similar content related to the search query.
- `get_contents`: Extracts content from the identified websites.

### 4. Write_Report_Agent

Create an extensive report on the cryptocurrency and generate a downloadable PDF document.

**Task:**
- Create a detailed report by integrating analyses from Market_Analysis_Agent, Technical_Analysis_Agent, and Sentiment_Analysis_Agent.
- Provide an additional comprehensive analysis based on the integrated data.

## Project Structure

- `main.py`: Main script to run the agents and orchestrate their tasks.
- `agents/`: Directory containing the implementations of all agents.
  - `market_analysis_agent.py`: Implementation of Market_Analysis_Agent.
  - `technical_analysis_agent.py`: Implementation of Technical_Analysis_Agent.
  - `sentiment_analysis_agent.py`: Implementation of Sentiment_Analysis_Agent.
  - `write_report_agent.py`: Implementation of Write_Report_Agent.
- `tools/`: Directory containing the tools used by the agents.
  - `extract_url.py`: Implementation of the Extract_url tool.
  - `scrap_data.py`: Implementation of the Scrap_data tool.
  - `take_ss.py`: Implementation of the Take_ss tool.
  - `get_pic_content.py`: Implementation of the Get_Pic_Content tool.
  - `search.py`: Implementation of the search tool.
  - `find_similar.py`: Implementation of the find_similar tool.
  - `get_contents.py`: Implementation of the get_contents tool.
- `reports/`: Directory where generated reports will be saved.
- `README.md`: This readme file.

## How to Run

1. **Setup Environment:**
   Ensure you have Python installed and set up a virtual environment.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Dependencies:**
   Install the required packages using pip.

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Main Script:**

   ```bash
   streamlit run main.py
   ```

