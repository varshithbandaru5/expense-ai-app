import streamlit as st
from model import predict_category
import pandas as pd
import re
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Smart Expense App", page_icon="💸", layout="wide")

# Title
st.title("💸 Smart Expense Categorizer")

# Sidebar
st.sidebar.title("📊 Navigation")
option = st.sidebar.radio("Go to:", ["Add Expense", "Dashboard"])

# Session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Expense", "Category", "Amount"])

# Extract amount
def extract_amount(text):
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0

# -------------------- ADD EXPENSE --------------------
if option == "Add Expense":
    st.header("➕ Add New Expense")

    user_input = st.text_input("Enter expense (e.g., Swiggy 300):")

    if st.button("Add Expense"):
        if user_input.strip() == "":
            st.warning("⚠️ Please enter an expense")
        else:
            result = predict_category(user_input)
            amount = extract_amount(user_input)

            st.success(f"Category: {result}")
            st.info(f"💰 Amount: ₹{amount}")

            new_data = pd.DataFrame([[user_input, result, amount]],
                                    columns=["Expense", "Category", "Amount"])
            st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# -------------------- DASHBOARD --------------------
elif option == "Dashboard":
    st.header("📊 Expense Dashboard")

    if st.session_state.data.empty:
        st.warning("No data available. Add some expenses first.")
    else:
        df = st.session_state.data

        # 🔥 METRICS (Top Cards)
        total_spent = df["Amount"].sum()
        total_transactions = len(df)

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Spending", f"₹{total_spent}")
        col2.metric("🧾 Total Transactions", total_transactions)

        # 🔥 CATEGORY SUMMARY
        st.subheader("📌 Category Summary")
        category_sum = df.groupby("Category")["Amount"].sum()

        cols = st.columns(len(category_sum))
        for i, (cat, amt) in enumerate(category_sum.items()):
            cols[i].metric(cat, f"₹{amt}")

        # 🔥 TABLE
        st.subheader("📋 Expense History")
        st.dataframe(df, use_container_width=True)

        # 🔥 CHARTS
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Category Count")
            st.bar_chart(df["Category"].value_counts())

        with col2:
            st.subheader("🥧 Spending Distribution")
            fig, ax = plt.subplots()
            ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
            st.pyplot(fig)

        # 🔥 RESET BUTTON
        if st.button("🗑 Reset All Data"):
            st.session_state.data = pd.DataFrame(columns=["Expense", "Category", "Amount"])
            st.success("All data cleared!")