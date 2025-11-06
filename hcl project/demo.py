import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Hotel Revenue Dashboard", layout="wide")

# Sidebar Styling with Date Range Filter
st.sidebar.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #2C3E50;
            padding: 20px;
            border-radius: 12px;
        }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
            color: #ECF0F1;
            font-family: Arial, sans-serif;
        }
        [data-testid="stSidebar"] .stDateInput > label {
            font-size: 16px;
            font-weight: bold;
            color: #ECF0F1;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📅 Date Range Filter")

# Load Data Function
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        file_path = "hotel_revenue_data_last_5_years.csv"
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            # Sample data
            data = {
                "Date": pd.date_range(start="2024-01-01", periods=10, freq='D'),
                "Revenue": [5000, 7000, 6500, 8000, 7200, 8900, 9300, 8500, 9100, 9400],
                "Occupancy": [75, 80, 78, 85, 82, 87, 90, 88, 86, 92]
            }
            df = pd.DataFrame(data)

    required_columns = {"Date", "Revenue", "Occupancy"}
    if not required_columns.issubset(df.columns):
        st.error("❌ Missing required columns in dataset. Please upload a valid file.")
        return None

    df["Date"] = pd.to_datetime(df["Date"])
    df["Hotel Name"] = "Hotel XYZ"
    return df

df = load_data()

# Sidebar Date Filter
if df is not None:
    min_date, max_date = df["Date"].min(), df["Date"].max()
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    # Filter data based on selected date range
    df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# Main Navigation for one-by-one view
st.title("🏨 Hotel Revenue Management Dashboard")

# 🏠 Overview
st.markdown("### 🏠 Overview: Key Performance Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="💰 Total Revenue", value=f"$ {df['Revenue'].sum():,.2f}")

with col2:
    st.metric(label="🏠 Average Occupancy", value=f"{df['Occupancy'].mean():.2f} %")

with col3:
    st.metric(label="📈 Highest Revenue", value=f"$ {df['Revenue'].max():,.2f}")

st.markdown("### Revenue & Occupancy Trends")
fig1 = px.line(df, x="Date", y="Revenue", title="💰 Revenue Over Time", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# 📈 Revenue Analysis
st.markdown("### 📈 Revenue Analysis")
fig2 = px.line(df, x="Date", y="Revenue", title="💰 Daily Revenue Trend", markers=True, color_discrete_sequence=["#FF5733"])
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(df, x="Revenue", title="📊 Revenue Distribution", nbins=10, color_discrete_sequence=["#3498DB"])
st.plotly_chart(fig3, use_container_width=True)

# 📊 Occupancy Analysis
st.markdown("### 📊 Occupancy Analysis")
fig4 = px.bar(df, x="Date", y="Occupancy", title="📊 Daily Occupancy Rate", text_auto=True, color="Occupancy", color_continuous_scale="Blues")
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.box(df, y="Occupancy", title="🏠 Occupancy Rate Distribution", points="all", color_discrete_sequence=["#2ECC71"])
st.plotly_chart(fig5, use_container_width=True)

# 📂 Upload Data
st.markdown("### 📂 Upload Revenue Data")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.write(df.head())
        st.success("✅ File uploaded successfully!")

# Download Updated CSV
st.sidebar.markdown("### 📥 Download Updated Data")
updated_file_path = "hotel_revenue_data_updated.csv"
df.to_csv(updated_file_path, index=False)
st.sidebar.download_button(label="📂 Download CSV", data=open(updated_file_path, "rb"), file_name="hotel_revenue_data_updated.csv", mime="text/csv")
