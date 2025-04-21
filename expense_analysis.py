import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(csv_file=None):
    # Check if a custom CSV file is provided
    if csv_file:
        if os.path.exists(csv_file):
            print(f"Loading data from {csv_file}...")
            return pd.read_csv(csv_file)
        else:
            print(f"Error: The file {csv_file} does not exist.")
            return None
    else:
        # Use the default sample data if no CSV file is provided
        default_file = 'sample_expenses.csv'
        print(f"Loading default data from {default_file}...")
        return pd.read_csv(default_file)

def analyze_data(df):
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Group by category and calculate total expenses
    category_expenses = df.groupby('Category')['Amount'].sum()

    # Plot and save pie chart
    category_expenses.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8))
    plt.title('Spending by Category')
    plt.savefig('spending_by_category.png')
    plt.close()

    # Plot total spending over time
    df.set_index('Date', inplace=True)
    df.resample('M')['Amount'].sum().plot(kind='line', figsize=(10, 6))
    plt.title('Total Spending Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.savefig('total_spending_over_time.png')

def main():
    # Prompt the user to enter a CSV file path
    csv_file = input("Enter the path to your CSV file (or press Enter to use the default): ").strip()

    # Load data
    df = load_data(csv_file)
    if df is not None:
        analyze_data(df)
        print("Analysis complete. Charts saved as PNG files.")

if __name__ == "__main__":
    main()
