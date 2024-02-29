# Import nececassary packages
import pandas as pd 
import plotly.express as px
import streamlit as st 

class EDA:

    def __init__(self, df):
        self.df = df

    def catconsep(self):
        df = self.df
        cat = list(df.columns[df.dtypes=='object'])
        con = list(df.columns[df.dtypes!='object'])
        return cat, con

    def univariate_hist(self, column):
        df = self.df
        fig = px.histogram(data_frame=df, x=column)
        return fig 

    def univariate_count(self, column):
        df = self.df 
        counts = df[column].value_counts().to_frame()
        counts.reset_index(level=0, inplace=True)       
        fig = px.bar(data_frame=counts, x=column, y='count')
        return fig

st.set_page_config(page_title='EDA - Utkarsh Gaikwad')

st.title('Automated EDA - Utkarsh Gaikwad')

option = st.sidebar.radio('Select Option',
                          ['Univariate', 'Bivariate', 'Multivariate'])

st.subheader('Upload File')
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write('Dataframe head')
    st.write(df.head())
    eda = EDA(df)
    cat, con = eda.catconsep()
    st.write(f'Categorical columns : {cat}')
    st.write(f'Continuous columns : {con}')
    st.write(f'Descriptive Analytics')
    st.write(df[con].describe().T)
    st.write(df[cat].describe().T)

if uploaded_file is not None:
    if option=='Univariate':
        st.subheader('Univariate Analysis')    
        col = st.selectbox('Select Column name :', tuple(df.columns))
        if col in con:
            fig1 = eda.univariate_hist(col)
            st.plotly_chart(fig1)
        else:
            fig1 = eda.univariate_count(col)
            st.plotly_chart(fig1)

        