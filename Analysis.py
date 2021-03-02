import matplotlib.pyplot as plt
import seaborn as sns
from table import create_table
import pandas as pd
import streamlit as st
import plotly.tools as tls
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px

import os
st.image('Somaiya Header.png',width=500)
st.title('Result analysis')
st.subheader('KJ somaiya institute of engineering and IT')
st.sidebar.title('Welcome to the result analyser App')
st.sidebar.markdown('<html><body style="background-color:yellow;"> You can Do <b>Visual</b> or <b>Database</b> analysis as you wish after filling the parameters select as required </body></html>'
                    ,unsafe_allow_html=True)
Analyse_type=st.sidebar.radio('Analyser',('Visual','Database Analyser','Reports'))


filename = st.text_input('Enter a file path:','Sem4.pdf')
Semester=st.text_input("Enter the No of semester",4)
Subject_no =st.text_input("enter the number of subjects",5)
Labs_no =st.text_input("enter the number of Labs",5)

@st.cache(persist=True)
def load_data():
    theory_df,pracs_df=create_table(filename,Subject_no,Labs_no)
    return theory_df,pracs_df

cleandf=load_data()[0]
pracsdf=load_data()[1]

if Analyse_type=='Visual':
    #Pie chart
    st.markdown('<html><h1><body style="background-color:orange;">Pie chart</body></h1></html>',unsafe_allow_html=True)
    explode=[0.1,0]
    colours=['lightgreen','Red']
    fig=px.pie(cleandf,labels=['Pass','Fail'],names='Pass/fail',title='Passing and failing percentage')
    #fig=cleandf['Pass/fail'].value_counts().plot(kind='pie',labels=['pass','fail'],autopct='%1.1f%%',startangle=140,
    #                                       explode=explode,shadow=True,colors=colours,figsize=(5,5))
    st.plotly_chart(fig)

    #Bar chart
    st.markdown('<html><h1><body style="background-color:pink;">Bar charts</body></h1></html>',unsafe_allow_html=True)
    plt.style.use('bmh')
    colors=['green','slateblue','mediumorchid','gold','darkorange','coral','yellow']
    k=1
    for i in range(int(Subject_no)):
        fig=plt.figure()
        #cleandf.iloc[:,k].plot(kind='hist',bins=3,color=colors[k])
        sns.distplot(cleandf.iloc[:,k],color=colors[k],norm_hist=True)
        plt.xlabel(f'Marks in {cleandf.columns[k]}')
        plt.ylabel('No of students')
        try:
            plotly_fig = tls.mpl_to_plotly(fig)
        except:
            subject=cleandf.columns[k]
            plotly_fig=px.histogram(cleandf,x=subject,histnorm='probability density',opacity=0.8,title=f'Marks in {cleandf.columns[k]}',color_discrete_sequence=['indianred'] )
        st.plotly_chart(plotly_fig)
        k=k+1
        if(k>int(Subject_no)):
            break

    #Bar chart Pracicals
    st.markdown('<html><h1><body style="background-color:cyan;">Bar charts for practicals</body></h1></html>',unsafe_allow_html=True)
    plt.style.use('bmh')
    colors=['green','slateblue','mediumorchid','gold','darkorange','coral','yellow']
    k=1
    for i in range(int(Subject_no)):
        fig=plt.figure()
        #cleandf.iloc[:,k].plot(kind='hist',bins=3,color=colors[k])
        sns.distplot(pracsdf.iloc[:,k],color=colors[k],norm_hist=True)
        plt.xlabel(f'Marks in {pracsdf.columns[k]}')
        plt.ylabel('No of students')
        try:
            plotly_fig = tls.mpl_to_plotly(fig)
        except:
            subject=pracsdf.columns[k]
            plotly_fig=px.histogram(pracsdf,x=subject,histnorm='probability density',opacity=0.8,title=f'Marks in {pracsdf.columns[k]}',color_discrete_sequence=['indianred'] )
        st.plotly_chart(plotly_fig)
        k=k+1
        if(k>int(Subject_no)):
            break

#Database
if Analyse_type=='Database Analyser':
    st.markdown('<html><h1><body style="background-color:Grey;">Database Analysis</body></h1></html>',
                 unsafe_allow_html=True)
    from database import create_database,query_execute
    create_database(cleandf,pracsdf,Semester)
    st.subheader(f'SQL Theory table for sem {Semester}' )
    query=st.text_input("enter a query for the sql databse",f'SELECT * FROM Sem_{Semester}_theory_results')
    #query=f'SELECT * FROM Sem_{Semester}_theory_results
    output=query_execute(query)
    st.dataframe(output)

    st.subheader(f'SQL practical table for sem {Semester}')
    query=st.text_input("enter a query for the sql databse",f'SELECT * FROM Sem_{Semester}_pracs_results')
    #query=f'SELECT * FROM Sem_{Semester}_pracs_results'
    output_pracs=query_execute(query)
    st.dataframe(output_pracs)

if Analyse_type=='Reports':
    #First class
    st.markdown('<html><h1><body style="background-color:cyan;">First class students</body></h1></html>',
                unsafe_allow_html=True)
    FC=cleandf[cleandf['CGPA']>=7.75]
    fc_students=FC.shape[0]
    st.dataframe(FC)
    st.write(f' There are {fc_students} students in first class')

    #Second class
    st.markdown('<html><h1><body style="background-color:cyan;">Second class students</body></h1></html>',
                unsafe_allow_html=True)
    SC=cleandf[(cleandf['CGPA']>=6.75) & (cleandf['CGPA']<=7.74)]
    st.dataframe(SC)
    sc_students=SC.shape[0]
    st.write(f' There are {sc_students}  students in second class')
    #pass class
    st.markdown('<html><h1><body style="background-color:cyan;">pass class students</body></h1></html>',
                unsafe_allow_html=True)
    PC=cleandf[(cleandf['CGPA']>=4.00) & (cleandf['CGPA']<=5.74)]
    st.dataframe(PC)
    pc_students=PC.shape[0]
    st.write(f' There are {pc_students}  students in pass class')

    #Top 5 scorers
    st.markdown('<html><h1><body style="background-color:blue;">Toppers</body></h1></html>',
                unsafe_allow_html=True)
    no_students = st.number_input('Number of students ', 6)
    column = 'CGPA'
    column=st.selectbox('select an attribute',
                 tuple(cleandf.columns)
    )

    bottom = False
    toppers = cleandf[column].sort_values(ascending=bottom).values
    toppers = list(toppers[0:no_students])
    st.dataframe(cleandf[cleandf[column].isin(toppers)].sort_values(by=[column], ascending=False))







