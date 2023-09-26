import streamlit as st
import pandas as pd
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
st.subheader("Let's review this survey.")


### load dataframe

file = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xls", "xlsx"]))

if file is not None:
    columns_to_use = [0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11]
    filename = file.name
    st.write(filename + " file uploaded")
    df = pd.read_csv(file, encoding="ISO-8859-1",usecols=columns_to_use, header=0)
    print(df)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce', downcast='integer')

    print(df)

       # st.dataframe(df)

    brands = df.groupby('Brand').size().reset_index(name='Count')
    brands.dropna(inplace=True) ## to avoid null values
    fueltypes= df.groupby('Fuel_Type').size().reset_index(name='Count')
    fueltypes.dropna(inplace=True) ## to avoid null values
    model= df['ModelName'].unique().tolist()
    brand= df['Brand'].unique().tolist()
    model_year= df['Model_Year'].unique().tolist()
    milage= df['Milage'].unique().tolist()
    fuel= df['Fuel_Type'].unique().tolist()
    engine= df['Engine'].unique().tolist()
    transmission= df['Transmission'].unique().tolist()
    Int_color= df['Int_Color'].unique().tolist()
    clean_title= df['Clean_Title'].unique().tolist()
    price= df['Price'].unique().tolist()

    default_fuel = df['Fuel_Type'].unique()[0:2] 
    fuel_selection = st.sidebar.multiselect('Fuel Type Used:', fuel, default=default_fuel)
    fuel_selection = [item for item in fuel_selection if item is not None]

    model_selection = st.sidebar.slider('Model_Year:', min_value=min(model_year),
                                    max_value= max(model_year),
                                    value=(min(model_year),max(model_year)))

    brand_selection = st.sidebar.multiselect('Pick your Brand',brand)
    if not brand_selection:
        df2= df.copy()
    else:
        df2 = df[df["Brand"].isin(brand_selection)]
    

    m_selection = st.sidebar.multiselect('Pick your Model',df2['ModelName'].unique())
    if not m_selection:
        df3= df2.copy()
    else:
        df3 = df2[df2["ModelName"].isin(m_selection)]

    if not brand_selection and not m_selection:
        filtered_df=df
    elif not m_selection:
        filtered_df=df[df["Brand"].isin(brand_selection)]
    elif not brand_selection:
        filtered_df=df[df["ModelName"].isin(m_selection)]
    elif brand_selection:
        filtered_df=df2[df2["Brand"].isin(brand_selection)]
    elif m_selection:
        filtered_df=df2[df2["ModelName"].isin(m_selection)]
    else:
        filtered_df=df2[df2["Brand"].isin(brand_selection) & df2["ModelName"].isin(m_selection)]

    fuel_df=filtered_df.groupby(by=["Fuel_Type"],as_index=False)["Price"].sum()
    print(fuel_df)

    with st.container():
        l1,r1= st.columns(2)

    with l1:
        st.subheader("FuleType WIse Price")
        
        # Format the 'Price' values as currency
        fuel_df['Formatted_Price'] = fuel_df['Price'].apply(lambda x: '${:,.2f}'.format(x))
        
        fig = px.bar(fuel_df, x="Fuel_Type", y="Price", text="Formatted_Price", template="seaborn")
        
        # Remove the temporary 'Formatted_Price' column
        fuel_df.drop(columns=['Formatted_Price'], inplace=True)
        
        st.plotly_chart(fig, use_container_width=True, height=200)
    # with r1:
    #     st.subheader("Model Wise Price")
    #     fig= px.pie(filtered_df, values="Price", names="Brand", hole=0.5)
    #     print(fig)
    #     fig.update_traces(text=filtered_df["Brand"],textposition='outside')
    #     st.plotly_chart(fig, use_container_width=True)

        
            







    # model_selection =st.sidebar.multiselect('Model Name:',model,default=model) 
 

    #mask df creation with the filter options
    mask= (df['Model_Year'].between(*model_selection)) & (df['Fuel_Type'].isin(fuel_selection))
    filtered_df = df[mask]
    number_of_Results=filtered_df.shape[0]
    st.markdown(f'*Available Results: {number_of_Results}*')


    AJ_df_grouped = filtered_df.groupby(by=['Fuel_Type']).count()[['ModelName']].reset_index()
    AJ_df_grouped.rename(columns={'ModelName': 'No.of Models'}, inplace=True)
    AJ_df_grouped.rename(columns={'Fuel_Type': 'Fuel Type Name'}, inplace=True)


    # plot bar chart
    with st.container():
        l_col,r_col=st.columns((1,2))
        with l_col:
            st.dataframe(AJ_df_grouped)
        with r_col:
            bar_chart= px.bar(AJ_df_grouped,
                            x="Fuel Type Name",
                            y="No.of Models",
                            color_discrete_sequence=['#F63366']*len(AJ_df_grouped),
                            template='plotly_white')
            bar_chart.update_layout(width=500)

            st.plotly_chart(bar_chart)



    st.markdown("---")
    # show employees cities in piechart
    st.title("Pie chart of year")


    pie_chart = px.pie(brands,
                    title="Brands",
                    values="Count",
                    names="Brand")

    st.plotly_chart(pie_chart)


    st.markdown("---")
    # show employees cities in piechart
    st.title("Pie chart")


    pie_chart = px.pie(fueltypes,
                    title="Transmissions",
                    values="Count",
                    names="Fuel_Type")

    st.plotly_chart(pie_chart)
    # st.dataframe(df[0:10])
    



else:
    st.write("No file uploaded yet.")











# streamlit slider 

















