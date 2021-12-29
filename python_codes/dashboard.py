from  oneM2M_functions import *
import json
import streamlit as st
import altair as alt
import pandas as pd
# from Crypto.Cipher import AES

server = "https://esw-onem2m.iiit.ac.in"
cse = "/~/in-cse/in-name/"
ae = "Team-5"

# key = "abcdefghijklmnop"
# cypher = AES.new(key, AES.MODE_ECB)

import struct, math

def do_encryption(a):
  return a^343

def do_decryption(a):
  return int(a)^343

setup = False
if setup:
    ae_lbl = ["AE-Label-1","AE-LABEL-2"]
    create_ae (server+cse,ae,ae_lbl)
    cnt_lbl = ["Label-1"]
    cnt_name = "Node-1"
    create_cnt(server+cse+ae,cnt_name,cnt_lbl)
    cnt_name = "Data-rpm"
    cnt_lbl = "Label-rpm_inp"
    create_cnt(server+cse+ae,cnt_name,cnt_lbl) 

lbl_Node1 = ["Label-1","Label-2"]   
lbl_Data1 = ["Label-1","Label-2"]  
global_spd = 300
with st.form(key='my_form'):
    spd = st.slider('Select input Speed in rpm ?',0,2000,400,50)
    global_spd= spd
    col1,col2,col3,col4,col5,col6,col7 = st.columns(7)
    with col1:
        submit_btn = st.form_submit_button(label='Submit')
    with col7:
        refresh1 = st.form_submit_button(label='Refresh')

with st.form('Form1'):
    prop = st.slider(label='kP', min_value=0, max_value=100, key=4 )
    inte = st.slider(label='kI', min_value=0, max_value=100, key=4 )
    deri = st.slider(label='kD', min_value=0, max_value=100, key=4 )
    col1,col2,col3,col4,col5,col6,col7 = st.columns(7)
    with col1:
        submit_param = st.form_submit_button('Submit Parameters')
    with col7:
        refresh2 = st.form_submit_button(label='Refresh')

if submit_btn:
    st.write(f'Speed is {spd} rpm')
    
    spd = do_encryption(spd)
    print("xor speed",spd)
    create_data_cin(server+cse+ae+"/"+"Node-1/Input-rpm",spd,lbl_Node1)
    _,val=get_data(server+cse+ae+"/Node-1/"+"Input-rpm?rcn=4")


############### Parameters 
if submit_param:
    st.write(f'Prop value is {prop} Integration value is {inte} Derivative value is {deri}')
    prop = do_encryption(prop)
    inte = do_encryption(inte)
    deri = do_encryption(deri)
    paramter_array= [prop,inte,deri] 
    create_data_cin(server+cse+ae+"/"+"Node-1/Parameters",paramter_array,lbl_Node1)
    _,val=get_data(server+cse+ae+"/Node-1/"+"Parameters?rcn=4")

if submit_btn or submit_param or refresh1 or refresh2:
    given_speed = global_spd
    _,motor_speed=get_data(server+cse+ae+"/Node-1/"+"Current-rpm-val?rcn=4")
    st.write(f'Given Speed is {given_speed} rpm')
    X_ax = []
    Y_ax = []
    Y_ax1 = []
    for i in motor_speed["m2m:cin"]:
        sped,timee=i['con'].split(',')
        X_ax.append(do_decryption(timee))
        Y_ax.append(do_decryption(sped))
        print("motor speed ",do_encryption(int(sped)))
        Y_ax1.append(given_speed)
    st.write(f'Current Speed is {Y_ax[len(Y_ax)-1]} rpm')

    print(X_ax)
    print(Y_ax)

    df = pd.DataFrame(
        {
            'Time': X_ax,
            'Current Speed': Y_ax,
            'Desired Speed': Y_ax1
        },
        columns=['Time', 'Current Speed', 'Desired Speed']
    )
    df = df.melt('Time', var_name='name', value_name='value')
    chart = alt.Chart(df).mark_line().encode(
    x=alt.X('Time:N'),
    y=alt.Y('value:Q'),
    color=alt.Color("name:N")
    ).properties(title="Speed vs Time")
    st.altair_chart(chart, use_container_width=True)

