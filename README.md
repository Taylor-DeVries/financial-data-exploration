# Personal Finance Dashboard

A modern, interactive dashboard for exploring and analyzing your personal financial data. Built with Streamlit, this app allows you to visualize spending patterns, track financial goals, and gain insights from your expenses—all with a beautiful, industry-standard UI.

---

## Features

- **Modern Dashboard UI:** Card-based layout, dark theme, and responsive design.
- **Flexible Data Input:** Upload your own CSV file or use built-in dummy data for demo/testing.
- **Key Metrics:** Instantly see your total net worth, total spending, and transaction count.
- **Financial Goal Tracking:** Set your net worth goal and visualize your progress.
- **Interactive Visualizations:**
  - Spending by Category (Pie Chart)
  - Spending Over Time (Line Chart)
  - Category Trends (Line Chart)
  - Spending Forecast (Linear Regression)
- **Raw Data Table:** Explore your filtered data directly in the app.
- **Easy Filtering:** Filter by date range and category.

---

## Demo

Visit the dashboard here: [personal-dashboard.streamlit.app](https://personal-dashboard.streamlit.app/)

![image](https://github.com/user-attachments/assets/efae9849-d1cd-4f9a-a9e8-cbb8924c0da7)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/financial-dashboard.git
cd financial-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

### 4. Use the Dashboard

- **Upload your CSV:** Use the sidebar to upload your expense data (CSV format).
- **Or use dummy data:** Click "Use Default/Dummy Data" to explore the dashboard with sample data.
- **Set your net worth and goal:** Enter your current net worth and your financial goal in the sidebar.
- **Explore:** Use filters and interact with the charts to analyze your finances.

---

## CSV Format

Your CSV should have at least these columns:
- `Date` (YYYY-MM-DD or similar)
- `Category` (e.g., Rent, Groceries, Entertainment)
- `Amount` (numeric, e.g., 120.50)

Example:
```csv
Date,Category,Amount
2024-01-01,Rent,800
2024-01-08,Groceries,120
...
```

---

## Customization

- **Dummy Data:** Easily tweak the sample data in `app.py` for demos or onboarding.
- **Add More Analytics:** The code is modular—add new charts or KPIs as needed.
- **Theming:** Adjust the CSS in `app.py` for your own color scheme or branding.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for all Python dependencies.

---

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Inspired by modern finance dashboards and UI best practices.
