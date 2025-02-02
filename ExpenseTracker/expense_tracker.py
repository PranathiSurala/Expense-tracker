import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Folder paths
data_folder = 'data'
output_folder = 'output'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to generate a financial report for all households
def generate_report():
    # Read the data
    data = pd.read_csv(os.path.join(data_folder, 'transactions.csv'))
    
    # Process data: Ensuring proper data types
    data['Mthly_HH_Income'] = pd.to_numeric(data['Mthly_HH_Income'], errors='coerce')
    data['Mthly_HH_Expense'] = pd.to_numeric(data['Mthly_HH_Expense'], errors='coerce')
    data['Emi_or_Rent_Amt'] = pd.to_numeric(data['Emi_or_Rent_Amt'], errors='coerce')
    data['Annual_HH_Income'] = pd.to_numeric(data['Annual_HH_Income'], errors='coerce')
    data['No_of_Fly_Members'] = pd.to_numeric(data['No_of_Fly_Members'], errors='coerce')
    data['No_of_Earning_Members'] = pd.to_numeric(data['No_of_Earning_Members'], errors='coerce')

    # Generate summaries for each household
    def generate_excel_report():
        # Save summary to Excel
        data_summary = data[['Mthly_HH_Income', 'Mthly_HH_Expense', 'Annual_HH_Income', 'Emi_or_Rent_Amt', 'No_of_Fly_Members', 'Highest_Qualified_Member', 'No_of_Earning_Members']]

        data_summary.to_excel(os.path.join(output_folder, 'financial_summary.xlsx'), index=False)

    def generate_pdf_report():
        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Household Financial Report", ln=True, align='C')
        pdf.ln(10)

        # Add Summary Data for all households
        pdf.set_font("Arial", size=12)
        for index, row in data.iterrows():
            pdf.cell(200, 10, txt=f"Household {index + 1}:", ln=True)
            pdf.cell(200, 10, txt=f"Monthly Household Income: {row['Mthly_HH_Income']}", ln=True)
            pdf.cell(200, 10, txt=f"Monthly Household Expense: {row['Mthly_HH_Expense']}", ln=True)
            pdf.cell(200, 10, txt=f"Annual Household Income: {row['Annual_HH_Income']}", ln=True)
            pdf.cell(200, 10, txt=f"EMI or Rent Amount: {row['Emi_or_Rent_Amt']}", ln=True)
            pdf.cell(200, 10, txt=f"Number of Flying Members: {row['No_of_Fly_Members']}", ln=True)
            pdf.cell(200, 10, txt=f"Highest Qualified Member: {row['Highest_Qualified_Member']}", ln=True)
            pdf.cell(200, 10, txt=f"Number of Earning Members: {row['No_of_Earning_Members']}", ln=True)
            pdf.ln(5)

        # Generate bar chart for Income vs. Expense
        plt.figure(figsize=(8, 6))
        plt.bar(data.index, data['Mthly_HH_Income'], width=0.4, label='Monthly Income', align='center')
        plt.bar(data.index, data['Mthly_HH_Expense'], width=0.4, label='Monthly Expense', align='edge')
        plt.xlabel('Household')
        plt.ylabel('Amount')
        plt.title('Income vs Expense')
        plt.legend()
        chart_path = os.path.join(output_folder, 'income_vs_expense.png')
        plt.savefig(chart_path)
        plt.close()

        # Add chart to PDF
        pdf.image(chart_path, x=10, y=pdf.get_y(), w=180)
        pdf.ln(90)  # Add space for next part

        # Generate pie chart for number of earning members distribution
        earning_members_count = data['No_of_Earning_Members'].value_counts()
        plt.figure(figsize=(7, 7))
        earning_members_count.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Earning Members Distribution')
        pie_chart_path = os.path.join(output_folder, 'earning_members_pie_chart.png')
        plt.savefig(pie_chart_path)
        plt.close()

        # Add pie chart to PDF
        pdf.image(pie_chart_path, x=10, y=pdf.get_y(), w=180)

        # Save the PDF
        pdf.output(os.path.join(output_folder, 'household_financial_report.pdf'))

    # Run the functions to generate reports
    generate_excel_report()
    generate_pdf_report()

    print("Reports generated successfully!")

# Example: Generate a financial report for all households
generate_report()
