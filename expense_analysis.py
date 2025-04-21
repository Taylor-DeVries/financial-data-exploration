import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('sample_expenses.csv')

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
