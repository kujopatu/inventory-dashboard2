import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.title("📦 Inventory Dashboard")

# Sample inventory data
data = {
    "Item": ["Product A", "Product B", "Product C"],
    "Stock Level": [50, 10, 5],
    "Reorder Level": [30, 20, 10]
}
df = pd.DataFrame(data)

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

# Export to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Inventory")
    processed_data = output.getvalue()
    return processed_data

st.subheader("Export Data")
excel_data = to_excel(df)
st.download_button(label="📥 Download as Excel", data=excel_data, file_name="inventory.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Visualization
st.subheader("📊 Inventory Charts")
fig, ax = plt.subplots()
sns.barplot(x=df["Item"], y=df["Stock Level"], ax=ax, palette="coolwarm")
ax.set_title("Stock Levels per Item")
ax.set_ylabel("Stock Level")
ax.set_xlabel("Item")
st.pyplot(fig)

# Line chart for stock trends
st.line_chart(df.set_index("Item")["Stock Level"])
