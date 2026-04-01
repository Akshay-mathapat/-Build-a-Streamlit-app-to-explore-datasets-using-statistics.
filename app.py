import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="📊 Data Explorer Pro", layout="wide")

# Custom CSS for UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">📊 Data Explorer Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your dataset & analyze like a Data Scientist</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show dataset
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_cols) == 0:
        st.warning("No numeric columns found!")
    else:
        column = st.sidebar.selectbox("Select Column", numeric_cols)
        data = df[column].dropna()

        # Metrics in columns
        st.subheader("📊 Key Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Mean", round(data.mean(), 2))
        col2.metric("Median", round(data.median(), 2))
        col3.metric("Std Dev", round(data.std(), 2))
        col4.metric("Variance", round(data.var(), 2))

        col5, col6 = st.columns(2)
        col5.metric("Min", data.min())
        col6.metric("Max", data.max())

        # Charts
        st.subheader("📈 Data Visualization")

        col7, col8 = st.columns(2)

        # Histogram
        with col7:
            st.write("Histogram")
            fig, ax = plt.subplots()
            sns.histplot(data, kde=True, ax=ax)
            st.pyplot(fig)

        # Boxplot
        with col8:
            st.write("Boxplot")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=data, ax=ax2)
            st.pyplot(fig2)

        # Insights
        st.subheader("🧠 Insights")

        if data.mean() > data.median():
            st.success("👉 Data is positively skewed (right-skewed)")
        elif data.mean() < data.median():
            st.warning("👉 Data is negatively skewed (left-skewed)")
        else:
            st.info("👉 Data is symmetric")

        if data.std() > data.mean() * 0.5:
            st.warning("👉 High variation in data")
        else:
            st.success("👉 Data is stable")

else:
    st.info("⬅️ Upload a CSV file from sidebar to begin")