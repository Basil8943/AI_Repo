import datetime
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image


st.set_page_config(page_title="Survey Results", page_icon=":tada:", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.header('Survey Results 2023')

# Load dataframe
file = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xls", "xlsx"])

if file is not None:
    # Specify the correct column names from your XLSX file
    expected_columns = [
        'Slno', 'OrderDate', 'ShipDate', 'Mode', 'CustomerName',
        'Country', 'City','State','PostalCode' 'Region', 'Category', 'SubCategory',
        'ProductName', 'Sales', 'Quantity', 'Discount', 'Profit','Segment',
    ]
    try:
        df = pd.read_excel(file, sheet_name='Sheet1', usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
        st.write("File uploaded and data loaded:")
        # st.write(df)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
    print(df)

    st.subheader("Let's review this survey.")
    st.markdown("---")

    mode=df['Mode'].unique().tolist()
    mode_selection = st.sidebar.multiselect('Ship Mode:', mode, default=mode)
    filtered_modedf = df[df['Mode'].isin(mode_selection)]

    category=df['Category'].unique().tolist()
    cat_selection = st.sidebar.multiselect('Ship Mode:', category, default=category)
    filtered_catdf = df[df['Category'].isin(cat_selection)]

    # Sales vs profit by category
    st.sidebar.title('Sales vs profit by category')
    fig = px.scatter(filtered_catdf, x='Sales', y='Profit', color='Category', title='Sales vs Profit')
    # Display the chart using st.plotly_chart
    st.plotly_chart(fig)

    # Sales in Each Shipmode
    fig = px.bar(filtered_modedf, x= 'Mode' , y='Segment', title='Sales in Each Mode')
    st.plotly_chart(fig)




    mode_selections = st.sidebar.multiselect('Select Modes:', df['Mode'].unique(), default=['Second Class', 'Standard Class'])
    filtered_df = df[df['Mode'].isin(mode_selection)]

    # Create a line chart comparing sales between selected modes
    fig = px.line(filtered_df, x='Category', y='SubCategory',color="Segment",title='Sales Comparison Between Mode and Region')
    st.plotly_chart(fig)


    fig = px.bar(filtered_df, x='Region', y='Sales', color='Mode', title='Sales Comparison Between Modes by Region')
    st.plotly_chart(fig)

    fig = px.scatter_3d(filtered_df, x='Region', y='Mode', z='Sales',
                    color='Sales', title='3D Surface Plot: Sales by Region and Mode')

    # Customize the layout if needed
    fig.update_layout(scene=dict(xaxis_title='Region', yaxis_title='Mode', zaxis_title='Sales'))
    # Show the plot
    st.plotly_chart(fig)


    fig = px.density_heatmap(filtered_df, x='Region', y='Mode', z='Sales',
                            title='Heatmap: Sales by Region and Mode',
                            marginal_x='histogram', marginal_y='histogram')

    # Customize the layout if needed
    fig.update_layout(xaxis_title='Region', yaxis_title='Mode')

    # Show the plot
    st.plotly_chart(fig)


    fig = px.violin(filtered_df, x='Region', y='Sales', color='Mode',
                title='Violin Plot: Sales Distribution by Region and Mode',
                box=True, points='all')

    # Customize the layout if needed
    fig.update_layout(xaxis_title='Region', yaxis_title='Sales')

    # Show the plot
    st.plotly_chart(fig)



    fig = px.sunburst(df, path=['Region', 'Mode'], values='Sales')

    # Set the title
    fig.update_layout(title='Sankey Diagram: Sales by Region and Mode')

    # Display the plot
    st.plotly_chart(fig)


