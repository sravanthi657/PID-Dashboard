from  oneM2M_functions import *
import json
import streamlit as st
import pandas
import numpy as np
import plotly.express as px
import plotly.graph_objects as gp
import pandas as pd
import time
from datetime import datetime

server = "http://127.0.0.1:8080"
cse = "/~/in-cse/in-name/"
ae = "Team-11"

setup = False
if setup:
    ae_lbl = ["AE-Label-1","AE-LABEL-2"]
    create_ae (server+cse,ae,ae_lbl)
    cnt_lbl = ["Label-1"]
    cnt_name = "Node-1"
    create_cnt(server+cse+ae,cnt_name,cnt_lbl)
    cnt_name = "Data"
    cnt_lbl = "Label-1"
    create_cnt(server+cse+ae,cnt_name,cnt_lbl) 

lbl_Node1 = ["Label-1","Label-2"]   
lbl_Data1 = ["Label-1","Label-2"]  

with st.form(key='my_form'):
    spd = st.slider('Select input Speed in rpm ?',0,2000,400,50)
    submit_btn = st.form_submit_button(label='Submit')

col1, col2, col3 = st.columns(3)

with col1:
    with st.form('Form1'):
        prop = st.slider(label='kP', min_value=0, max_value=50, key=4)
        submitted1 = st.form_submit_button('Submit kP')
with col2:
    with st.form('Form2'):
        inte = st.slider(label='kI', min_value=0, max_value=50, key=4)
        submitted2 = st.form_submit_button('Submit kI')
with col3:
    with st.form('Form3'):
        deri = st.slider(label='kD', min_value=0, max_value=50, key=4)
        submitted3 = st.form_submit_button('Submit kD')

if submit_btn:
    st.write(f'Speed is {spd} rpm')
    create_data_cin(server+cse+ae+"/"+"Node-1/Input",spd,lbl_Node1)
    _,val=get_data(server+cse+ae+"/Node-1/"+"Data?rcn=4")
    # print("val ",val)
    #for i in val["m2m:cnt"]:
    # a1,a2=i['con'].split(',')
        #a1 = i['con']
       # print("in loop ------> ",a1)
        # X_ax.append(float(a1))

############### Parameters
paramter_array= [prop,inte,deri]  
if submitted1:
    st.write(f'Proportional value is {prop} ')
    create_data_cin(server+cse+ae+"/"+"Node-1/Parameters",paramter_array,lbl_Node1)
    # _,val=get_data(server+cse+ae+"/Node-1/"+"Parameters?rcn=4")
    # print(val)
if submitted2:
    st.write(f'Integral value is {inte} ')
    create_data_cin(server+cse+ae+"/"+"Node-1/Parameters",paramter_array,lbl_Node1)
    # _,val=get_data(server+cse+ae+"/Node-1/"+"Parameters?rcn=4")
    # print(val)
if submitted3:
    st.write(f'Derivative value is {deri} ')
    create_data_cin(server+cse+ae+"/"+"Node-1/Parameters",paramter_array,lbl_Node1)
    # _,val=get_data(server+cse+ae+"/Node-1/"+"Parameters?rcn=4")
    # print(val)

    X_ax=[]
    Y_ax=[]



df = pd.DataFrame({

  'date': ['10/1/2019','10/2/2019', '10/3/2019', '10/4/2019','10/5/2019','10/6/2019','10/7/2019','10/8/2019','10/9/2019','10/10/2019','10/11/2019'],
  'second column': [10,7, 5,40,3, 20,50,73,4 ,30, 40]
})
df = df.rename(columns={'date':'index'}).set_index('index')
# df
st.line_chart(df)


    # Y_ax.append(float(a2)) 
    
    # print(X_ax)
    # print(Y_ax)
    # print(len(Y_ax))
    # X_ax,Y_ax =zip(*sorted(zip(X_ax,Y_ax)))
    # df = pandas.DataFrame(dict(
    #     X_axis = X_ax,
    #     Y_axis = Y_ax
    # ))
    # fig = px.line(
    #     df,
    #     x = "X_axis",
    #     y = "Y_axis",
    #     title = "line frame"
    # )
    # fig.update_traces(line_color = "blue")
    # st.plotly_chart(fig)

