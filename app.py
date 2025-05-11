import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# Font Awesome CDN for icons
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    body, .main, .stApp {
        background-color: #18192b !important;
        color: #fff !important;
    }
    .card {
        background-color: #23243a;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        margin-bottom: 1rem;
        color: #fff;
        text-align: center;
    }
    .kpi-title {
        font-size: 1.1rem;
        color: #aaa;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4ade80;
        max-width: 100%;
        word-break: break-all;
        overflow-wrap: break-word;
        white-space: normal;
        display: block;
    }
    .fa-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #7dd3fc;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        color: #fff;
    }
    .notification {
        background: #2d2e4a;
        border-left: 5px solid #f87171;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #fff;
    }
    .progress-bar {
        background: #23243a;
        border-radius: 0.5rem;
        height: 1.2rem;
        width: 100%;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .progress {
        background: #a78bfa;
        height: 100%;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
def load_data(uploaded_file=None):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        st.error("Please upload a CSV file.")
        return None

# --- KPI Calculations ---
def calculate_kpis(df):
    total_spending = df['Amount'].sum()
    avg_transaction = df['Amount'].mean()
    num_transactions = len(df)
    top_category = df.groupby('Category')['Amount'].sum().idxmax()
    available_balance = max(0, 15000 - total_spending)  # Example logic
    net_worth = 278378  # Placeholder
    return {
        'Available Balance': available_balance,
        'Total Net Worth': net_worth,
        'Total Spending': total_spending,
        'Average Transaction': avg_transaction,
        'Number of Transactions': num_transactions,
        'Top Spending Category': top_category
    }

# --- Analytics & Plots ---
def plot_spending_by_category(df):
    category_spending = df.groupby('Category')['Amount'].sum().reset_index()
    fig = px.pie(category_spending, values='Amount', names='Category',
                 title='', hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(paper_bgcolor='#23243a', plot_bgcolor='#23243a', font_color='#fff', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_total_spending_over_time(df):
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_spending = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_spending['Month'] = monthly_spending['Month'].astype(str)
    fig = px.line(monthly_spending, x='Month', y='Amount',
                  title='', labels={'Amount': 'Total Spending ($)', 'Month': 'Month'},
                  color_discrete_sequence=['#f87171'])
    fig.update_layout(paper_bgcolor='#23243a', plot_bgcolor='#23243a', font_color='#fff')
    st.plotly_chart(fig, use_container_width=True)

def plot_income_vs_expense(df):
    if 'Type' not in df.columns:
        st.info("No 'Type' column found. Skipping Income vs Expense chart.")
        return
    df['Month'] = df['Date'].dt.to_period('M')
    monthly = df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
    monthly['Month'] = monthly['Month'].astype(str)
    fig = px.bar(monthly, x='Month', y='Amount', color='Type', barmode='group',
                 color_discrete_map={'Income': '#4ade80', 'Expense': '#f87171'})
    fig.update_layout(paper_bgcolor='#23243a', plot_bgcolor='#23243a', font_color='#fff')
    st.plotly_chart(fig, use_container_width=True)

def plot_category_trends(df):
    df['Month'] = df['Date'].dt.to_period('M')
    category_monthly = df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
    category_monthly['Month'] = category_monthly['Month'].astype(str)
    fig = px.line(category_monthly, x='Month', y='Amount', color='Category',
                  title='', labels={'Amount': 'Spending ($)', 'Month': 'Month'})
    fig.update_layout(paper_bgcolor='#23243a', plot_bgcolor='#23243a', font_color='#fff')
    st.plotly_chart(fig, use_container_width=True)

def forecast_spending(df):
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_spending = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_spending['Month'] = monthly_spending['Month'].astype(str)
    X = np.arange(len(monthly_spending)).reshape(-1, 1)
    y = monthly_spending['Amount'].values
    model = LinearRegression()
    model.fit(X, y)
    future_months = np.arange(len(monthly_spending), len(monthly_spending) + 3).reshape(-1, 1)
    predictions = model.predict(future_months)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_spending['Month'],
        y=monthly_spending['Amount'],
        name='Actual Spending',
        mode='lines+markers',
        line=dict(color='#f87171')
    ))
    future_dates = pd.date_range(
        start=pd.to_datetime(monthly_spending['Month'].iloc[-1]),
        periods=4,
        freq='M'
    )[1:]
    fig.add_trace(go.Scatter(
        x=future_dates.strftime('%Y-%m'),
        y=predictions,
        name='Forecast',
        mode='lines+markers',
        line=dict(dash='dash', color='#a78bfa')
    ))
    fig.update_layout(
        title='',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        paper_bgcolor='#23243a',
        plot_bgcolor='#23243a',
        font_color='#fff',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_assets():
    # Example static data
    assets = pd.DataFrame({
        'Asset': ['Gold', 'Stock', 'Warehouse', 'Land'],
        'Value': [15700, 22500, 120000, 135000]
    })
    fig = px.pie(assets, values='Value', names='Asset', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(paper_bgcolor='#23243a', plot_bgcolor='#23243a', font_color='#fff', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def filter_data_by_date(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# --- Main App ---
def app():
    st.markdown('<h1 style="color:#fff;">Personal Finance Dashboard</h1>', unsafe_allow_html=True)
    st.sidebar.header('Navigation')
    # --- User Inputs ---
    st.sidebar.header('Your Financial Info')
    user_net_worth = st.sidebar.number_input(
        'Current Net Worth ($)',
        min_value=0,
        value=0,
        step=1000
    )
    user_goal = st.sidebar.number_input(
        'Financial Goal ($)',
        min_value=0,
        value=0,
        step=1000
    )
    uploaded_file = st.sidebar.file_uploader("Upload your expense data (CSV)", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.sidebar.header('Filters')
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.sidebar.date_input(
                'Select Date Range',
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            all_categories = ['All'] + list(df['Category'].unique())
            selected_category = st.sidebar.selectbox('Select Category', all_categories)
            if len(date_range) == 2:
                filtered_df = filter_data_by_date(df, date_range[0], date_range[1])
                if selected_category != 'All':
                    filtered_df = filtered_df[filtered_df['Category'] == selected_category]
            else:
                filtered_df = df
            kpis = calculate_kpis(filtered_df)
            # --- KPI Cards (remove Available Balance) ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="card"><div class="fa-icon"><i class="fa-solid fa-piggy-bank"></i></div><div class="kpi-title">Total Net Worth</div><div class="kpi-value">${user_net_worth:,.2f}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="card"><div class="fa-icon"><i class="fa-solid fa-money-bill-trend-up"></i></div><div class="kpi-title">Total Spending</div><div class="kpi-value">${kpis["Total Spending"]:,.2f}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="card"><div class="fa-icon"><i class="fa-solid fa-receipt"></i></div><div class="kpi-title">Transactions</div><div class="kpi-value">{kpis["Number of Transactions"]:,}</div></div>', unsafe_allow_html=True)
            # --- Progress Bar Example ---
            st.markdown('<div class="section-title">Financial Goal Progress</div>', unsafe_allow_html=True)
            percent = int((user_net_worth / user_goal) * 100) if user_goal > 0 else 0
            st.markdown(f'<div style="color:#a78bfa;font-size:1.2rem;">{percent}% of Goal</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="progress-bar"><div class="progress" style="width:{percent}%;"></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:#fff;">${user_net_worth:,.2f} / {user_goal:,}</div>', unsafe_allow_html=True)
            # --- Main Analytics ---
            st.markdown('<div class="section-title">Spending by Category</div>', unsafe_allow_html=True)
            plot_spending_by_category(filtered_df)
            st.markdown('<div class="section-title">Total Spending Over Time</div>', unsafe_allow_html=True)
            plot_total_spending_over_time(filtered_df)
            st.markdown('<div class="section-title">Category-wise Trends</div>', unsafe_allow_html=True)
            plot_category_trends(filtered_df)
            st.markdown('<div class="section-title">Spending Forecast</div>', unsafe_allow_html=True)
            forecast_spending(filtered_df)
            st.markdown('<div class="section-title">Raw Data</div>', unsafe_allow_html=True)
            st.dataframe(filtered_df.sort_values('Date', ascending=False), use_container_width=True)

if __name__ == "__main__":
    app()
