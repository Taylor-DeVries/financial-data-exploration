import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(uploaded_file=None):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        st.error("Please upload a CSV file.")
        return None

def plot_spending_by_category(df):
    category_spending = df.groupby('Category')['Amount'].sum()
    fig, ax = plt.subplots(figsize=(8, 8))
    category_spending.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Spending by Category')
    st.pyplot(fig)

def plot_total_spending_over_time(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_spending = df.groupby('Month')['Amount'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_spending.plot(kind='line', ax=ax)
    ax.set_title('Total Spending Over Time')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Spending')
    st.pyplot(fig)

def filter_data_by_date(df, start_date, end_date):
    # Convert start_date and end_date to datetime64[ns] if they are not already
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Now perform the comparison
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    return filtered_df


def app():
    st.title('Personal Finance Dashboard')

    # File upload
    uploaded_file = st.file_uploader("Upload your expense data (CSV)", type=["csv"])
    
    # Check if file is uploaded
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Show data
        if df is not None:
            st.write("### Raw Data", df.head())

            # Category Filter
            category = st.selectbox('Select Category', df['Category'].unique())
            st.write(f"Showing data for category: {category}")
            category_df = df[df['Category'] == category]
            st.write("### Filtered Data", category_df)

            # Spending by category pie chart
            plot_spending_by_category(df)

            # Total spending over time chart
            plot_total_spending_over_time(df)

            # Date Range Filter
            st.subheader('Filter by Date Range')
            start_date = st.date_input('Start Date', df['Date'].min())
            end_date = st.date_input('End Date', df['Date'].max())

            if start_date and end_date:
                filtered_df = filter_data_by_date(df, start_date, end_date)
                st.write("### Filtered Data", filtered_df)

                # Plot for filtered data
                plot_total_spending_over_time(filtered_df)

if __name__ == "__main__":
    app()
