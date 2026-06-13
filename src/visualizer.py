import matplotlib.pyplot as plt
import seaborn as sns

def generate_financial_dashboard(final_benchmark_table, output_path="reports/financial_dashboard.png"):
    """
    Pipeline Step 4: Generates the 2x2 grid framework dashboard and exports it to PNG.
    """
    print(" Rendering Financial Peer Dashboard...")

    #  Separate the real companies from the peers average row for clean plotting
    companies_data = final_benchmark_table[final_benchmark_table["Company"] != "PEER_AVG"]
    peers_avg_data = final_benchmark_table[final_benchmark_table["Company"] == "PEER_AVG"]

    # Set up a professional 2x2 grid of subplots, Matplotlib creates an internal 2D array (a grid table) of plot windows
    # thus the axes configuration down below to include the four variables
    # plt.subplots handles the layout grid. figsize is (width, height) in inches.
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle("TECH PEER BENCHMARKING DASHBOARD (Historical vs peers Average)", fontsize=16, fontweight="bold")

    # Create a configuration list mapping our columns to chart titles and grid positions 
    # the variable 'metrics' will choose a column to represent, then give the graph a title based on this name, then choose the grid emplacement to plot it
    metrics = [
        {"col": "Revenue_Growth_Pct", "title": "Revenue Growth (%)", "ax": axes[0, 0]},
        {"col": "Operating_Margin_Pct", "title": "Operating Margin (%)", "ax": axes[0, 1]},
        {"col": "Current_Ratio", "title": "Current Ratio (Liquidity)", "ax": axes[1, 0]},
        {"col": "PE_Ratio", "title": "P/E Ratio (Valuation)", "ax": axes[1, 1]}
    ]

    # Loop through our metrics list and draw the charts dynamically
    for m in metrics:
        # A. Plot the individual companies as solid lines with circular markers ('o')
        sns.lineplot(
            data=companies_data, x="Year", y=m["col"], hue="Company", 
            marker="o", linewidth=2.5, ax=m["ax"]
        )
        
        # B. Plot our Sample Average as a thick, dashed black line for a clear benchmark reference
        sns.lineplot(
            data=peers_avg_data, x="Year", y=m["col"], color="black", 
            linestyle="--", linewidth=3, label="PEERS AVERAGE", ax=m["ax"]
        )
        
        # C. Apply professional clean styling to each individual subplot
        m["ax"].set_title(m["title"], fontsize=12, fontweight="bold")
        m["ax"].set_ylabel(m["title"])
        m["ax"].set_xlabel("Fiscal Year")
        m["ax"].grid(True, linestyle="--", alpha=0.5)
        
        # Force years to display cleanly as integers (e.g., 2024) instead of floats (2024.0)
        years = sorted(final_benchmark_table["Year"].unique())
        m["ax"].set_xticks(years)
        m["ax"].set_xticklabels([str(int(y)) for y in years])

    # 5. Clean up the padding between charts so nothing overlaps
    plt.tight_layout()

    # Save configuration to the specified output directory path
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches
