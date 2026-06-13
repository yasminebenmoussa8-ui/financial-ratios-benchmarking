# Financial Ratios Automation & Peer Benchmarking Engine

An automated quantitative analysis pipeline that extracts multi-statement financial data via the Yahoo Finance API, calculates cross-pillar corporate performance metrics, and compiles an executive-ready PDF benchmark report with data visualizations.

##  Live Dashboard Preview
Cross-pillar performance vectors (Growth, Profitability, Liquidity, Valuation) compared against the sector average:

src/financial_dashboard.png

##  System Architecture & Workflow
- **Data Ingestion (`src/data_loader.py`):** Programmatically connects to `yfinance` to fetch financial matrices. Aligns Balance Sheets, Income Statements, and Cash Flow metrics via time-series index anchoring.
- **Analytics Engine (`src/metrics_engine.py`):** Evaluates core metrics across Growth, Profitability, Liquidity, and Market Valuation pillars, synthesizing a dynamic sector benchmark average.
- **Visualizer (`src/visualizer.py`):** Constructs a professional 2x2 grid charting layout using Matplotlib and Seaborn, comparing performance vectors against the peer universe.
- **Compilation Engine (`src/report_generator.py`):** Automates multi-statement table parsing, NaN protection handles, and visual elements into a publication-quality corporate PDF report via `fpdf2`.

## Execution Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/yasminebenmoussa8.ui/financial-ratios-benchmarking.git](https://github.com/yasminebenmoussa8.ui/financial-ratios-benchmarking.git)
2. pip install -r requirements.txt
3. python main.py
