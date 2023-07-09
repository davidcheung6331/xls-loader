import pandas as pd
import plotly.express as px
import streamlit as st 

# PANDAS DATABASE CREATION
st.set_page_config(
  page_title="Sales Dashboard",
  page_icon=":bar_chart:",
  layout="wide"                 
)

@st.cache_data
def get_data_from_excel():
    print(">>> get excel file")
    df= pd.read_excel(
      io='supermarkt_sales.xlsx',
      engine='openpyxl',
      sheet_name='Sales',
      skiprows=3,
      usecols='B:R',
      nrows=1000,
    )
    # Add 'hour' column to dataframe for second barchart
    df["hour"]=pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df


################################
# Create dataframe from excel file
################################
df=get_data_from_excel()


print("Create sidebar")
# SIDEBAR
st.sidebar.header("Please Filter Here:")
print("UI Create multiselect -  City Column")
city= st.sidebar.multiselect(
  "Select the City:",
  options=df["City"].unique(),
  default=df["City"].unique()
)

print("UI Create multiselect -  Customer type Colun")
customer_type= st.sidebar.multiselect(
  "Select the Customer Type:",
  options=df["Customer_type"].unique(),
  default=df["Customer_type"].unique()
)
print("Create unqiue/distinct value for Gender type selection by df")
gender= st.sidebar.multiselect(
  "Select the Gender:",
  options=df["Gender"].unique(),
  default=df["Gender"].unique()
)

st.sidebar.write("Excel data:")
st.sidebar.write(df.head(10))


print("Create a new dataframe df_selection with columns list :  @city & Customer_type== @customer_type & Gender == @gender")
df_selection=df.query(
  "City== @city & Customer_type== @customer_type & Gender == @gender"
)




# MAINPAGE
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

################################
# Summary Row
################################
print("Calucate sum, mean of total , rating column")
total_sales= int(df_selection["Total"].sum())
average_rating =round(df_selection["Rating"].mean(),1)
star_rating=":star:" * int(round(average_rating,0))
average_sale_by_transaction=round(df_selection["Total"].mean(),2)

print("Make the 3 columns of Header row")
# KPI's COLUMNS
left_column,middle_column,right_column=st.columns(3)

# make a row with 3 columns
with left_column:
  st.subheader("Total Sales:")
  st.subheader(f"US $ {total_sales:,}")
with middle_column:
  st.subheader("Average Rating:")
  st.subheader(f"{average_rating} - {star_rating}")
with right_column:
  st.subheader("Average Sales Per Transaction:")
  st.subheader(f"US $ {average_sale_by_transaction}")

  

st.markdown("---")









# BARCHARTS

# SALES BY PRODUCT LINE [BAR CHART]

sales_by_product_line=(
  df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)



fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#205295"] * len(sales_by_product_line),
    template="plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# SALES BY HOUR [BAR CHART]

sales_by_hour=df_selection.groupby(by=["hour"]).sum()[["Total"]]
# st.caption("sales by hour")
# st.write(sales_by_hour.head(5))


fig_hourly_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#205295"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


# Displaying charts
left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_product_sales,use_container_width=True)
right_column.plotly_chart(fig_hourly_sales,use_container_width=True)


# HIDE STREAMLIT STYLE
hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)