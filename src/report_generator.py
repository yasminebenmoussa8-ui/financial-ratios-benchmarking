import fpdf
from fpdf.enums import XPos, YPos
import pandas as pd
import os

class FinancialReport(fpdf.FPDF): #creation of our own version of the class fpdf

    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(30, 64, 175)
        self.cell(0,12,"Financial Peer Benchmark Report",new_x=XPos.LMARGIN,new_y=YPos.NEXT,align="C") #a cell which display the title
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0,10,f"Page {self.page_no()}/{{nb}}",align="C")


def create_pdf_report(final_benchmark_table, company_tickers, image_path="reports/financial_dashboard.png", output_dir="reports"):
    """
    Pipeline Step 5: Automates corporate reporting compilation into a clean multi-page PDF.
    """
    try:
        print("Beginning PDF creation...")

        output_path = os.path.join(output_dir, "Financial_Benchmark_Report.pdf")
        pdf = FinancialReport()

        pdf.alias_nb_pages() #to count the number of pages

        pdf.add_page() #starts with header

        # INTRODUCTION

        pdf.set_font("Helvetica", "", 11)

        intro = ("This report presents a peer benchmarking analysis "
            "of Microsoft, Apple, Alphabet and Meta. "
            "Financial ratios have been computed from annual "
            "financial statements retrieved via Yahoo Finance "
            "and analyzed using Python.")

        pdf.multi_cell(0, 6, intro) #the text of introduction takes numerous cells

        pdf.ln(5) #Line break

        # COMPANIES ANALYZED

        pdf.set_font("Helvetica", "B", 13)

        pdf.cell(0,10,"1. Companies Analyzed",new_x=XPos.LMARGIN,new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "", 11)

        for ticker in company_tickers:

            pdf.cell(0,7,f"- {ticker}",new_x=XPos.LMARGIN,new_y=YPos.NEXT)

        # PAGE 2

        pdf.add_page()

        pdf.set_font("Helvetica", "B", 13)

        pdf.cell(0,10,"2. Key Financial Ratios",new_x=XPos.LMARGIN,new_y=YPos.NEXT)

        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 8)

        headers = ["Company","Year","Revenue Growth","Op Margin","Current Ratio","PE"]

        widths = [25, 15, 35, 35, 30, 25]

        for h, w in zip(headers, widths):
            pdf.cell(w, 8, h, border=1)

        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        
        # ==============================================================================
        # DESIGN NOTE: DATA EXTRACTION & FORMATTING MECHANISM FOR THE PDF TABLE
        # ==============================================================================
        # The loop 'for _, row in final_benchmark_table.iterrows():' processes the 
        # Pandas DataFrame row-by-row like a conveyor belt. 
        #
        # At each iteration, specific metrics (like 'Revenue_Growth_Pct') are extracted 
        # into temporary variables (e.g., 'growth') to serve two critical purposes:
        #
        # 1. ANTI-CRASH PROTECTION ('pd.isna'): Financial data sometimes contains empty 
        #    cells (NaN). FPDF will crash if it tries to print a NaN value. Storing the 
        #    data first allows us to check if the cell is empty; if it is, we cleanly 
        #    print 'N/A' instead of crashing the pipeline.
        #
        # 2. PROFESSIONAL FORMATTING ('.2f'): Raw numbers from Python often contain 
        #    too many decimal places (e.g., 14.285714...). The variable allows us to 
        #    apply an f-string format ('{growth:.2f}') to restrict the display to 
        #    exactly two clean decimal places (e.g., 14.29) for a corporate look.
        #
        # Note on 'int(row["Year"])': Years are cast to integers first to strip away 
        # any trailing decimals (converting '2022.0' to '2022') before being converted 
        # to a string ('str') for FPDF compatibility.
        # ==============================================================================

        for _, row in final_benchmark_table.iterrows(): #takes one row at a time

            pdf.cell(widths[0], 8, str(row["Company"]), border=1)

            pdf.cell(widths[1], 8, str(int(row["Year"])), border=1)

            growth = row["Revenue_Growth_Pct"]

            pdf.cell(widths[2],8,"N/A" if pd.isna(growth) else f"{growth:.2f}",border=1)

            margin = row["Operating_Margin_Pct"]

            pdf.cell( widths[3],8,"N/A" if pd.isna(margin) else f"{margin:.2f}",border=1)

            current_ratio = row["Current_Ratio"]

            pdf.cell(widths[4],8,"N/A" if pd.isna(current_ratio) else f"{current_ratio:.2f}", border=1)

            pe = row["PE_Ratio"]

            pdf.cell(widths[5],8,"N/A" if pd.isna(pe) else f"{pe:.2f}",border=1)

            pdf.ln()

        # PAGE 3 DASHBOARD

        pdf.add_page()

        pdf.set_font("Helvetica", "B", 13)

        pdf.cell(0,10,"3. Financial Dashboard",new_x=XPos.LMARGIN,new_y=YPos.NEXT)

        pdf.image(image_path, x=10, y=35, w=190)

        # PAGE 4 CONCLUSION

        pdf.add_page()

        pdf.set_font("Helvetica", "B", 13)

        pdf.cell(0,10,"4. Key Findings",new_x=XPos.LMARGIN,new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "", 11)

        pdf.multi_cell(0,7,
            (
                "- Revenue growth was benchmarked against the peer average.\n"
                "- Operating margin highlights profitability differences.\n"
                "- Current ratio measures liquidity strength.\n"
                "- PE ratio compares market valuation levels.\n"
                "- The analysis was fully automated using Python."
            )
        )

        pdf.output(output_path) #the conclusion text

        print("PDF successfully generated")
        print(f"Saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"ERROR: {e}")
        return None
