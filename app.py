import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Load data from the Excel file
df = pd.read_excel("Adidas US Sales Datasets.xlsx")

# Configure the Streamlit app layout to use a wide format
st.set_page_config(layout="wide")

# Custom CSS to reduce padding around the Streamlit block container
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load the Adidas logo
image = Image.open('adidas_logo.jpg')

# Create a two-column layout for the logo and dashboard title
col1, col2 = st.columns([0.2, 0.8])  # Column proportions

with col1:
    st.image(image, width=120)  # Display the Adidas logo

with col2:
    # Define a custom HTML title with CSS for styling
    html_title = """
        <style>
        .title-test {
            font-weight: bold;
            font-size: 2.5rem;  /* Title font size */
            margin-top: 10px;   /* Margin above title */
            color: #333333;     /* Dark color for contrast */
        }
        </style>
        <center><h1 class="title-test">Adidas US Interactive Sales Dashboard</h1></center>
    """
    st.markdown(html_title, unsafe_allow_html=True)

# Add a section for the last updated date
col3, col4, col5 = st.columns([0.1, 0.45, 0.45])  # Three-column layout
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))  # Current date
    st.write(f"Last updated by:  \n {box_date}")  # Display the last update

# Bar chart: Total Sales by Retailer
with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales",
                 labels={"TotalSales": "Total Sales {$}"},
                 title="Total Sales by Retailer", hover_data=["TotalSales"],
                 template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

# Expanders and Download buttons for Retailer-wise sales
_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])  # Layout
with view1:
    expander = st.expander("Retailer-wise Sales")  # Expander for data view
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()  # Group sales by retailer
    expander.write(data)

with dwn1:
    # Add a button to download retailer sales data
    st.download_button("Get Data", data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

# Line chart: Total Sales Over Time
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")  # Format date column to month-year
result = df.groupby(by="Month_Year")["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", 
                   title="Total Sales Over Time", template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

# Expander and download button for monthly sales
with view2:
    expander = st.expander("Monthly Sales")
    data = result  # Monthly sales data
    expander.write(data)

with dwn2:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")

st.divider()  # Add a horizontal divider for better organization

# Bar and line chart: Total Sales and Units Sold by State
result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

fig3 = go.Figure()
# Add total sales as a bar chart
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales"))
# Add units sold as a line chart on a secondary y-axis
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode="lines",
                          name="Units Sold", yaxis="y2"))
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),  # Secondary y-axis
    template="gridon",
    legend=dict(x=1, y=1.1)  # Adjust legend position
)
_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

# Expander and download button for state-wise sales data
_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)

with dwn3:
    st.download_button("Get Data", data=result1.to_csv().encode("utf-8"), 
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")

st.divider()

# Treemap: Total Sales by Region and City
_, col7 = st.columns([0.1, 1])
treemap = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    # Format sales in lakhs for display
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path=["Region", "City"], values="TotalSales",
                  hover_name="TotalSales (Formatted)",
                  hover_data=["TotalSales (Formatted)"],
                  color="City", height=700, width=600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4, use_container_width=True)

# Expander and download button for region and city-wise sales
_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])
with view4:
    result2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by Region and City")
    expander.write(result2)

with dwn4:
    st.download_button("Get Data", data=result2.to_csv().encode("utf-8"),
                                        file_name="Sales_by_Region.csv", mime="text/csv")

# Raw sales data view and download button
_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])
with view5:
    expander = st.expander("View Sales Raw Data")
    expander.write(df)

with dwn5:
    st.download_button("Get Raw Data", data=df.to_csv().encode("utf-8"),
                       file_name="SalesRawData.csv", mime="text/csv")
st.divider()
