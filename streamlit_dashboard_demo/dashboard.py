import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
from data import get_sample_data, forecast_sales
from mail_utils import send_feedback_email

def show_dashboard():
    st.set_page_config(page_title="Streamlit Dashboard", layout="wide")
    st.title("📊 Streamlit Dashboard with Full Features")

    st.sidebar.header("⚙️ Controls")
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    if st.sidebar.button("🔁 Increment Counter"):
        st.session_state.counter += 1

    name = st.sidebar.text_input("Enter your name")
    rating = st.sidebar.slider("Rate this dashboard", 1, 5, 3)
    region = st.sidebar.selectbox("Select Region", options=["All", "East", "West", "North", "South"])
    uploaded_file = st.sidebar.file_uploader("📥 Upload CSV", type="csv")

    df = pd.read_csv(uploaded_file) if uploaded_file else get_sample_data()
    if region != "All":
        df = df[df['Region'] == region]

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${df['Sales'].sum()}")
    col2.metric("📈 Avg Profit", f"${df['Profit'].mean():.2f}")
    col3.metric("📊 Records", len(df))

    st.plotly_chart(px.bar(df, x='Month', y='Sales', color='Region'), use_container_width=True)
    st.altair_chart(alt.Chart(df).mark_line().encode(x='Month', y='Profit', color='Region'), use_container_width=True)

    st.subheader("📊 Matplotlib Pie Chart")
    fig2, ax = plt.subplots()
    df.groupby("Region")["Sales"].sum().plot.pie(autopct='%1.1f%%', ax=ax)
    st.pyplot(fig2)

    with st.expander("🗃 View Raw Data"):
        st.dataframe(df)

    st.download_button("📤 Download CSV", df.to_csv(index=False).encode("utf-8"), "export.csv", "text/csv")

    st.subheader("📈 Sales Forecast (Next 3 Months)")
    forecast_df = forecast_sales(df, steps=3)
    st.line_chart(pd.concat([df[['Sales']], forecast_df[['SalesForecast']].rename(columns={"SalesForecast": "Sales"})], ignore_index=True))

    with st.form("feedback_form"):
        feedback = st.text_area("💬 Any suggestions?")
        submitted = st.form_submit_button("Submit")
        if submitted:
            success = send_feedback_email(feedback, name or "Anonymous")
            if success:
                st.success("📩 Feedback submitted and emailed!")
            else:
                st.warning("⚠️ Failed to send email. Please check SMTP settings.")

    st.caption(f"👤 User: {name or 'Anonymous'} | ⭐ Rating: {rating} | 🔄 Counter: {st.session_state.counter}")