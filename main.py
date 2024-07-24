from crewai import Crew
import streamlit as st
from fpdf import FPDF
from agents import CryptoTradingAgents
from tasks import CryptoTradingTasks


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

    filename = "analysis_report.pdf"
    pdf.output(filename)

    return filename


if __name__ == "__main__":
    main()
