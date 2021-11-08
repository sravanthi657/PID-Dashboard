from  oneM2M_functions import *
import json
import streamlit as st
import pandas
import numpy as np
import plotly.express as exp
import plotly.graph_objects as gp


server = "http://127.0.0.1:8080"
cse = "/~/in-cse/in-name/"
ae = "AE-PID"

setup = False
if setup:
    ae_lbl = ["AE-Label-1","AE-LABEL-2"]
    create_ae (server+cse,ae,ae_lbl)
    cnt_lbl = ["Label-1"]
    cnt_name = "Node-1"
    create_cnt(server+cse+ae,cnt_name,cnt_lbl)
    cnt_name = "Data-1"
    cnt_lbl = "Label-1"
    create_cnt(server+cse+ae,cnt_name,cnt_lbl) 

lbl_Node1 = ["Label-1","Label-2"]   
lbl_Data1 = ["Label-1","Label-2"]  

with st.form(key='my_form'):
    spd = st.slider('Select input Speed in rpm ?',100,200,300,400)
    submit_btn = st.form_submit_button(label='Submit')

if submit_btn:
    st.write(f'Speed is {spd} rpm')
    create_data_cin(server+cse+ae+"/"+"Node-1",spd,lbl_Node1)
    _,val=get_data(server+cse+ae+"/"+"Data-1?rcn=4")
    print(val)
    X_ax=[]
    Y_ax=[]
    for i in val["m2m:cnt"][m2m:cin]:
        a1,a2=i['con'].split(',')
        X_ax.append(float(a1))  
        Y_ax.append(float(a2)) 
    print(X_ax)
    print(Y_ax)
    print(len(Y_ax))
    X_ax,Y_ax =zip(*sorted(zip(X_ax,Y_ax)))
    df = pandas.DataFrame(dict(
        X_axis = X_ax,
        Y_axis = Y_ax
    ))
    fig = px.line(
        df,
        x = "X_axis",
        y = "Y_axis",
        title = "line frame"
    )
    fig.update_traces(line_color = "blue")
    st.plotly_chart(fig)