from crewai import Crew
import streamlit as st
from fpdf import FPDF
from PIL import Image
from agents import CryptoTradingAgents
from tasks import CryptoTradingTasks
from PIL import Image
import os


def crop_image(number):
    image_path = 'gauge.jpeg'
    image = Image.open(image_path)

    # Define the crop area (left, upper, right, lower)
    crop_box = (10, 10, 2700, 1700)

    # Crop the image
    cropped_image = image.crop(crop_box)

    # Save or display the cropped image
    cropped_image.save(f'gauge_{number}.jpeg')
    



def main():
    st.title("Cryptocurrency Analysis Report")

    coin_name = st.text_input("Enter the coin name:").encode('utf-8').decode('utf-8')


    if st.button("Run Analysis"):
        agents = CryptoTradingAgents()
        tasks = CryptoTradingTasks()
        file_path = "gauge.jpeg"

        Market_Analysis_Agent = agents.Market_Analysis_Agent()
        Technical_Analysis_Agent = agents.Technical_Analysis_Agent()
        Moving_Average_Analysis_Agent = agents.Moving_Average_Analysis_Agent()
        Closing_Price_Analysis_Agent = agents.Closing_Price_Analysis_Agent()
        Sentiment_Analysis_Agent = agents.Sentiment_Analysis_Agent()
        Report_Agent = agents.Report_Agent()
        Gauge_Agent1 = agents.Gauge_Agent1()
        Gauge_Agent2 = agents.Gauge_Agent2()
        Gauge_Agent3 = agents.Gauge_Agent3()

        Perform_Market_Analysis = tasks.Perform_Market_Analysis(Market_Analysis_Agent, coin_name)
        Perform_Chart_Analysis = tasks.Perform_Chart_Analysis(Technical_Analysis_Agent, coin_name)
        Moving_Average_Analysis = tasks.Moving_Average_Analysis(Moving_Average_Analysis_Agent, coin_name)
        Closing_Price_Analysis = tasks.Closing_Price_Analysis(Closing_Price_Analysis_Agent, coin_name)
        Get_News = tasks.Get_News(Sentiment_Analysis_Agent, coin_name)
        Write_Rport = tasks.Write_Rport(Report_Agent)
        Create_Gauge1 = tasks.Create_Gauge1(Gauge_Agent1)
        Create_Gauge2 = tasks.Create_Gauge2(Gauge_Agent2)
        Create_Gauge3 = tasks.Create_Gauge3(Gauge_Agent3)

        
        Create_Gauge1.context = [Perform_Chart_Analysis]
        Create_Gauge2.context = [Moving_Average_Analysis]
        Write_Rport.context = [Perform_Market_Analysis, Perform_Chart_Analysis, Get_News]
        Create_Gauge3.context = [Write_Rport]


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
        image = Image.open("coin_screenshot.jpeg")
        st.image(image, caption='Technical Analysis', use_column_width=True)
        


        crew3 = Crew(
            
            agents=[Gauge_Agent1],
            tasks=[Create_Gauge1],
            verbose=True

            )
        
        result3 = crew3.kickoff()
        st.subheader("Gauge Results")
        st.write(result3)
        crop_image(1)
        image = Image.open("gauge_1.jpeg")
        st.image(image, caption='Gaugemeter for Technical Analysis', use_column_width=True)
        os.remove(file_path)


        crew4 = Crew(

            agents = [Moving_Average_Analysis_Agent],
            tasks = [Moving_Average_Analysis],
            verbose = True
        )
        result4 = crew4.kickoff()
        st.subheader("Moving Average Analysis Results")
        st.write(result4)
        image = Image.open("sma.jpeg")
        st.image(image, caption='Moving Average Chart', use_column_width=True)


        crew5 = Crew(
            
            agents=[Gauge_Agent2],
            tasks=[Create_Gauge2],
            verbose=True

            )
        
        result5 = crew5.kickoff()
        st.subheader("Gauge Results")
        st.write(result5)
        crop_image(2)
        image = Image.open("gauge_2.jpeg")
        st.image(image, caption='Gaugemeter for Moving Average', use_column_width=True)
        os.remove(file_path)
        
        crew6 = Crew(
            
            agents=[Closing_Price_Analysis_Agent],
            tasks=[Closing_Price_Analysis],
            verbose=True

            )
        
        result6 = crew6.kickoff()
        st.subheader("Closing Chart Results")
        st.write(result6)
        image = Image.open("line_chart.jpeg")
        st.image(image, caption = 'Closing Chart', use_column_width=True)


        
        crew7 = Crew(
            
            agents=[Sentiment_Analysis_Agent],
            tasks=[Get_News],
            verbose=True

            )

        result7 = crew7.kickoff()
        st.subheader("Sentiment Analysis Results")
        st.write(result7)

        crew8 = Crew(
            
            agents=[Report_Agent],
            tasks=[Write_Rport],
            verbose=True

            )

        result8 = crew8.kickoff()
        st.subheader("Final Report")
        st.write(result8)

        crew9 = Crew(
            
            agents=[Gauge_Agent3],
            tasks=[Create_Gauge3],
            verbose=True

            )
        
        result9 = crew9.kickoff()
        st.subheader("Gauge Results")
        st.write(result9)
        crop_image(3)
        image = Image.open("gauge_3.jpeg")
        st.image(image, caption='Gaugemeter for Summary', use_column_width=True)
        os.remove(file_path)


        # Save results to PDF
        pdf_file = save_to_pdf(result1, result2, result3, result4, result5, result6, result7, result8, result9)
        st.success(f"Results saved to {pdf_file}")

        # Add download button
        with open(pdf_file, "rb") as f:
            pdf_data = f.read()

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=pdf_file,
            mime="application/pdf",
        )

def save_to_pdf(result1, result2, result3, result4, result5, result6, result7, result8, result9):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("DejaVu", "", "DejaVuSansCondensed.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "DejaVuSansCondensed-Bold.ttf", uni=True)

    def write_unicode(text, size=12, style=""):
        pdf.set_font("DejaVu", style=style, size=size)
        lines = text.split('\n')
        for line in lines:
            if line.startswith('####'):
                pdf.set_font("DejaVu", style="B", size=14)
                pdf.multi_cell(0, 10, line[5:].strip())
            elif '**' in line:
                parts = line.split('**')
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        pdf.set_font("DejaVu", style="", size=size)
                    else:
                        pdf.set_font("DejaVu", style="B", size=size)
                    pdf.write(5, part)
                pdf.ln()
            else:
                pdf.multi_cell(0, 5, line)
        pdf.ln(5)

    write_unicode("Market Analysis Results:", size=16, style="B")
    write_unicode(str(result1))
    pdf.add_page()

    write_unicode("Technical Analysis Results:", size=16, style="B")
    write_unicode(str(result2))
    pdf.add_page()
    pdf.image("coin_screenshot.jpeg", x=10, y=pdf.get_y(), w=190)
    pdf.add_page()

    write_unicode("Gauge Results (Technical Analysis):", size=16, style="B")
    pdf.image("gauge_1.jpeg", x=10, y=pdf.get_y(), w=190)
    pdf.add_page()

    write_unicode("Moving Average Analysis Results:", size=16, style="B")
    write_unicode(str(result4))
    pdf.add_page()
    pdf.image("sma.jpeg", x=10, y=pdf.get_y(), w=190)
    pdf.add_page()

    write_unicode("Gauge Results (Moving Average):", size=16, style="B")
    write_unicode(str(result5))
    pdf.image("gauge_2.jpeg", x=10, y=pdf.get_y(), w=190)
    pdf.add_page()

    write_unicode("Closing Chart Results:", size=16, style="B")
    write_unicode(str(result6))
    pdf.add_page()
    pdf.image("line_chart.jpeg", x=10, y=pdf.get_y(), w=190)
    pdf.add_page()

    write_unicode("Sentiment Analysis Results:", size=16, style="B")
    write_unicode(str(result7))
    pdf.add_page()

    write_unicode("Final Report:", size=16, style="B")
    write_unicode(str(result8))
    pdf.add_page()

    write_unicode("Gauge Results (Summary):", size=16, style="B")
    write_unicode(str(result9))
    pdf.image("gauge_3.jpeg", x=10, y=pdf.get_y(), w=190)

    filename = "analysis_report.pdf"
    pdf.output(filename)
    return filename


if __name__ == "__main__":
    main()
