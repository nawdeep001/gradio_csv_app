import matplotlib.pyplot as plt

def generate_plot(csv_data, x_column, y_column):
    """Generates a scatter plot for the selected columns."""
    if csv_data is None:
        return "Please upload a CSV file first."

    if x_column not in csv_data.columns or y_column not in csv_data.columns:
        return f"Invalid column selection: {x_column}, {y_column}"

    plt.figure(figsize=(6, 4))
    plt.scatter(csv_data[x_column], csv_data[y_column], alpha=0.5)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column}")
    plt.savefig("plot.png")
    return "plot.png"
