import matplotlib.pyplot as plt
import os

def generate_graph(df, graph_type, title):
    """
    Generates and saves professional graphs based on Aadhaar analysis output.
    """
    # Plotting style set karein
    plt.style.use('seaborn-v0_8-muted') # Ya 'ggplot' use karein
    
    # Output folder ensure karo
    output_dir = "data/output/graphs"
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(14, 7))

    # Data check: Ensure df is not empty
    if df.empty:
        print(f"Warning: {title} ke liye dataframe empty hai.")
        return

    # ---------- BAR GRAPH ----------
    if graph_type == "bar":
        # Usually first col is category, last is the metric
        x_col = df.columns[0]
        y_col = df.columns[-1]

        # Top 15 districts/states dikhana better hai readability ke liye
        df_sorted = df.sort_values(by=y_col, ascending=False).head(15)

        bars = plt.bar(df_sorted[x_col], df_sorted[y_col], color='skyblue', edgecolor='navy')
        plt.xlabel(x_col.replace('_', ' ').title())
        plt.ylabel(y_col.replace('_', ' ').title())
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval):,}', 
                     va='bottom', ha='center', fontsize=9)

    # ---------- LINE GRAPH (Time Series) ----------
    elif graph_type == "line":
        # Longitudinal/Temporal analysis ke liye
        x_col = df.columns[0]
        y_cols = [c for c in df.columns if c != x_col]

        for col in y_cols:
            plt.plot(df[x_col].astype(str), df[col], marker='o', linewidth=2, label=col)

        plt.xlabel("Time Period")
        plt.ylabel("Enrollment Count")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()

    # Graph formatting
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save graph
    file_name = title.replace(" ", "_").lower() + ".png"
    file_path = os.path.join(output_dir, file_name)

    plt.savefig(file_path, dpi=300) # Professional quality (300 DPI)
    plt.close()

    print(f"Graph saved at: {file_path}")