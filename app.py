# Import nececassary packages
import pandas as pd 
import plotly.express as px
import streamlit as st 
import seaborn as sns

class EDA:

    def __init__(self, df):
        self.df = df

    def catconsep(self):
        df = self.df
        cat = list(df.columns[df.dtypes=='object'])
        con = list(df.columns[df.dtypes!='object'])
        return cat, con

    def univariate(self, column):
        df = self.df
        cat, con = self.catconsep()
        if column in con:
            fig = px.histogram(data_frame=df, x=column)
            st.write(f'Histogram for {column}')
            st.plotly_chart(fig)
        else:            
            counts = df[column].value_counts().to_frame()
            counts.reset_index(level=0, inplace=True)       
            fig = px.bar(data_frame=counts, x=column, y='count')
            st.write(f'Count Plot for {column}')
            st.plotly_chart(fig)

    def bivariate(self, column1, column2):
        df = self.df
        cat, con = self.catconsep()
        if column1 in con and column2 in con:
            fig = px.scatter(data_frame=df, x=column1, y=column2)
            st.write(f'Scatterplot for {column1} vs {column2}')
            st.plotly_chart(fig)
        elif column1 in con and column2 in cat:
            fig = px.box(data_frame=df, x=column2, y=column1, color=column2)
            st.write(f'Boxplot for {column1} and {column2}')
            st.plotly_chart(fig)
        elif column1 in cat and column2 in con:
            fig = px.box(data_frame=df, x=column1, y=column2, color=column1)
            st.write(f'Boxplot for {column1} and {column2}')
            st.plotly_chart(fig)
        elif column1 in cat and column2 in cat:
            ctab = pd.crosstab(df[column1], df[column2])
            fig = px.imshow(ctab, text_auto=True)
            st.write(f'Crosstab Heatmap for {column1} vs {column2}')
            st.plotly_chart(fig)

    def multivariate_corr(self):
        cat, con = self.catconsep()
        corr = self.df[con].corr()
        fig = px.imshow(corr, text_auto=True)
        st.write('Correlation Heatmap')
        st.plotly_chart(fig)

    def multivariate_pairplot(self, color):
        df = self.df
        fig = sns.pairplot(data=df, hue=color)
        st.pyplot(fig)

st.set_page_config(page_title='EDA - Utkarsh Gaikwad')

st.title('Automated EDA - Utkarsh Gaikwad')

option = st.sidebar.radio('Select Option',
                          ['Descriptive', 'Univariate', 'Bivariate', 'Multivariate'])

st.subheader('Upload File')
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    eda = EDA(df)
    cat, con = eda.catconsep()
    if option=='Descriptive':        
        st.write('Dataframe head')
        st.write(df.head())   
        st.write(f'Categorical columns : {cat}')
        st.write(f'Continuous columns : {con}')
        st.write('Missing Values :')
        m = df.isna().sum().to_frame()
        st.write(m)
        st.write('Duplicate Values')
        d = df.duplicated().sum()
        st.write(d)
        st.write(f'Descriptive Analytics')
        st.write(df[con].describe())
        st.write(df[cat].describe())
    elif option=='Univariate':
        st.subheader('Univariate Analysis')    
        col = st.selectbox('Select Column name :', tuple(df.columns))
        eda.univariate(col)
    elif option=='Bivariate':
        st.subheader('Bivariate Analysis')
        col1 = st.selectbox('Select Column 1 : ', tuple(df.columns))
        col2 = st.selectbox('Select Column 2 : ', tuple(df.columns))
        eda.bivariate(col1, col2)
    elif option=='Multivariate':
        st.subheader('Multivariate Analysis')
        opt = st.selectbox('What multivariate analysis you want?',('pairplot', 'correlation'))
        if opt=='pairplot':                    
            c = st.selectbox('Provide categorical column for color : ', cat)
            st.write('Pariplot for Data')
            b = st.button('Plot')
            if b:
                with st.spinner('Work in Progress'):
                    eda.multivariate_pairplot(c)
                st.success('Done')
        else:
            eda.multivariate_corr()  
        