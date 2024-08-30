import pandas as pd
import plotly.express as px
import streamlit as st



st.set_page_config(page_title="Automted EDA Analytics Portal",
                   page_icon="📊"
                   )

# Title of the application
st.title(":rainbow[Data Analytics Webiste]")
st.subheader(':gray[Explore Data with ease]', divider="rainbow")


file = st.file_uploader("Please drop your csv or excel file", type=['csv', 'xlsx'])
if file != None:
    if file.name.endswith ('csv'):
        data = pd.read_csv(file,  encoding='utf-8', errors = 'ignore')
    else:
        data = pd.read_excel(file, engine= 'python', encoading = 'latin, errors='ignore')

    st.dataframe(data)
    st.info("File is successfully uploaded", icon="🚨")

    st.subheader(":rainbow[Basic information of the dataset]", divider='rainbow')
    tab1, tab2,tab3, tab4 = st.tabs(["Summary", "Top and Bottom rows", "Data Types", "Columns"])
    
    with tab1:
        st.write(f"There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset")
        st.subheader(":gray[Statistical Summary of the Dataset]")
        st.dataframe(data.describe())

    with tab2:
        st.subheader(":gray[Top rows]")
        toprows = st.slider("Number of rows you want", 1, data.shape[0], key="topslider")
        st.dataframe(data.head(toprows))

        st.subheader(":gray[Bottom rows]")
        bottomrows = st.slider("Number of rows you want", 1, data.shape[0], key="bottomslider")
        st.dataframe(data.tail(bottomrows))
    
    with tab3:
        st.subheader(":gray[Data dtypes of the columns]")
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader("Name of the columns")
        st.write(list(data.columns))

    st.subheader(":rainbow[Columns Values To Count]", divider='rainbow')
    with st.expander("Value Counts"):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox("Choose Column Name", options=list(data.columns))
        with col2:
            toprows = st.number_input("Top Rows", min_value=1, step=1)

        count = st.button("Count")
        if count == True:
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader("Visualization", divider='gray')
            fig = px.bar(data_frame=result, x=column, y = 'count', text='count', template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result, x = column, y = 'count', text='count', template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result, names=column, values='count')
            st.plotly_chart(fig)

    st.subheader(":rainbow[Groupby : Simplify your Data Analysis]", divider='rainbow')
    st.write("The groupby let's you summarize by specific category or groups")
    with st.expander("Group by your columns"):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect("Choose your column to groupby", options=list(data.columns))
        with col2:
            operation_col = st.selectbox("Choose column for operation", options=list(data.columns))
        with col3:
            operation = st.selectbox("Choose operation to perform", options=['sum', 'max', 'min', 'mean', 'median', 'count', 'std'])

        if groupby_cols:
                result = data.groupby(groupby_cols).agg(
                    newcol = (operation_col, operation)
                ).reset_index()

                st.dataframe(result)

                st.subheader(":gray[Data Visualization]", divider='gray')
                graphs = st.selectbox("Choose your graph", options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
                if graphs == 'line':
                    x_axis = st.selectbox('Choose x axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose y axis', options=list(result.columns))
                    color = st.selectbox("Choose Information",options= [None] + list(result.columns))
                    fig = px.line(data_frame=result, x = x_axis, y = y_axis, color=color, markers='o')
                    st.plotly_chart(fig)

                elif graphs == 'bar':
                    x_axis = st.selectbox('Choose x axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose y axis', options=list(result.columns))
                    color = st.selectbox("Choose Information",options= [None] + list(result.columns))
                    facet_col = st.selectbox("Columns Information", options=[None] + list(result.columns))  
                    fig = px.bar(data_frame=result, x = x_axis, y = y_axis, color=color, facet_col=facet_col, barmode='group')
                    st.plotly_chart(fig)

                elif graphs == 'scatter':
                    x_axis = st.selectbox('Choose x axis', options=list(result.columns))
                    y_axis = st.selectbox('Choose y axis', options=list(result.columns))
                    color = st.selectbox("Choose Information",options= [None] + list(result.columns))
                    size = st.selectbox("Size column", options=[None] + list(result.columns))
                    fig = px.scatter(data_frame=result, x= x_axis, y = y_axis, color= color, size=size)
                    st.plotly_chart(fig)

                elif graphs == 'pie':
                    values = st.selectbox("Choose numerical values", options=list(result.columns))
                    names = st.selectbox("Choose labels", options=list(result.columns))
                    fig = px.pie(data_frame=result, values=values, names=names)
                    st.plotly_chart(fig)

                elif graphs == 'sunburst':
                    path = st.multiselect("Choose your Path", options=list(result.columns))
                    fig = px.sunburst(data_frame=result, path = path, values='newcol')
                    st.plotly_chart(fig)



