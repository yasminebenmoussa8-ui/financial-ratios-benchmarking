from src.data_loader import fetch_financial_statements
from src.metrics_engine import calculate_financial_ratios, build_benchmark_table
from src.visualizer import generate_financial_dashboard
from src.report_generator import create_pdf_report

def main():
    print("==================================================")
    print("  Financial Ratios Benchmarking Engine Launch     ")
    print("==================================================\n")
    
    # step 1 : companies selection
    tickers = ["MSFT", "AAPL", "GOOGL", "META"]
    
    # step 2 : financial data raw extraction
    print("[Pipeline 1/5] Extracting statements from Yahoo Finance...")
    raw_ratios_dict = fetch_financial_statements(tickers)
    
    # step 3 : financial ratio calculation
    print("\n[Pipeline 2/5] Running financial metrics computing engine...")
    calculated_ratios_dict = calculate_financial_ratios(raw_ratios_dict, tickers)
    final_benchmark_table = build_benchmark_table(calculated_ratios_dict)
    
    # step 4 : benchmark creation
    print("\n[Pipeline 3/5] Generating professional 2x2 grid charts...")
    dashboard_path = "reports/financial_dashboard.png"
    generate_financial_dashboard(final_benchmark_table, output_path=dashboard_path)
    
    # step 5 : pdf report creation
    print("\n[Pipeline 4/5] Compiling automated PDF financial report...")
    pdf_path = create_pdf_report(final_benchmark_table, image_path=dashboard_path)
    
    print("         Workflow Pipeline Run Terminated         ")
    print(f"       Report generated at: {pdf_path} ")

if __name__ == "__main__":
    main()