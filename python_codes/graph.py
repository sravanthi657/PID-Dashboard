import streamlit as st

import pandas as pd

import time

millis = str(round(time.time() * 1000))

from datetime import datetime

dateTimeObj = datetime.now()

timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")

df = pd.DataFrame({

'date': [timestampStr, millis],

'second column': [10, 20]

})

df = df.rename(columns={'date':'index'}).set_index('index')

st.line_chart(df)