import streamlit as st
import pandas as pd

# -----------------------
# PAGE CONFIGURATION
# -----------------------
st.set_page_config(
    page_title="Anzoo Stocks Intelligence Dashboard",
    layout="wide",
    page_icon="📈"
)

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\surya\Desktop\LORVENS\Dexter\AI insight on stocks\stock_fundamentals_with_insights.csv")
    return df

df = load_data()

st.title("📊 Anzoo AI — Stock Intelligence Dashboard")
st.caption("Smart financial insights powered by LangChain + Groq")

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔎 Filter Stocks")

# Search by company name
search = st.sidebar.text_input("Search Company", "")

# Filter by P/E Ratio range
pe_min, pe_max = st.sidebar.slider(
    "Select P/E Ratio Range", 
    min_value=float(df["P/E Ratio"].min()), 
    max_value=float(df["P/E Ratio"].max()), 
    value=(float(df["P/E Ratio"].min()), float(df["P/E Ratio"].max()))
)

# Apply filters
filtered_df = df[
    (df["P/E Ratio"] >= pe_min) &
    (df["P/E Ratio"] <= pe_max) &
    (df["Company Name"].str.contains(search, case=False))
]

# -----------------------
# MAIN TABLE
# -----------------------
st.subheader("📈 Stock Overview")

st.dataframe(
    filtered_df[[
        "Symbol", 
        "Company Name", 
        "Price (USD)", 
        "Market Cap (Billion USD)", 
        "P/E Ratio", 
        "Dividend Yield (%)", 
        "Next Earnings Date"
    ]],
    use_container_width=True
)

# -----------------------
# DETAILED INSIGHT VIEW
# -----------------------
st.subheader("💬 AI Insights")

selected_company = st.selectbox("Select a company for detailed insight", filtered_df["Company Name"])

if selected_company:
    company_row = filtered_df[filtered_df["Company Name"] == selected_company].iloc[0]

    st.markdown(f"### 🏢 {company_row['Company Name']} ({company_row['Symbol']})")
    st.markdown(f"**Price:** ${company_row['Price (USD)']}  |  **P/E Ratio:** {company_row['P/E Ratio']}  |  **Market Cap:** {company_row['Market Cap (Billion USD)']}B")
    st.markdown(f"**Dividend Yield:** {company_row['Dividend Yield (%)']}%  |  **Next Earnings:** {company_row['Next Earnings Date']}")
    st.markdown("---")
    st.markdown(f"🧠 **AI Insight:** {company_row['AI Insight']}")

# st.markdown("---")
# st.caption("Built with ❤️ by Surya Vennapu | Powered by LangChain + Gemini")
