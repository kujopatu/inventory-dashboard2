import streamlit as st
import pandas as pd

# Sample inventory data
data = {
    "Item": ["Product A", "Product B", "Product C"],
    "Stock Level": [50, 10, 5],
    "Reorder Level": [30, 20, 10]
}
df = pd.DataFrame(data)

st.title("📦 Inventory Dashboard")

# Display inventory table
st.subheader("Current Inventory Levels")
st.dataframe(df, hide_index=True)

# Update stock levels
st.subheader("Update Stock Levels")
for i in range(len(df)):
    new_stock = st.number_input(f"Update stock for {df['Item'][i]}", min_value=0, value=df['Stock Level'][i])
    df.at[i, "Stock Level"] = new_stock

# Highlight low stock items
def highlight_low_stock(row):
    return "🔴 LOW STOCK" if row["Stock Level"] <= row["Reorder Level"] else "✅ Sufficient"

df["Status"] = df.apply(highlight_low_stock, axis=1)

st.subheader("Updated Inventory Status")
st.dataframe(df, hide_index=True)
