import streamlit as st
import pandas as pd
import numpy as np
import os
import regex as re

PATH = os.getcwd()+'//results//output_thesis.txt'

#Functions
def file_check(name):
  #if os.path.exists(os.getcwd()+'\\results\\'+name):
  if os.path.exists(name):
    st.session_state.data_integrity = 1 
    st.warning('Файл существует', icon="❇️")
  else:
    st.session_state.data_integrity = 0
    st.warning('Файла не существует.\nПроверьте написание имени.', icon="✴️")

@st.cache_data
def file_load(name):
  if st.session_state.data_integrity == 0:
    st.warning('Проверка наличия файла не пройдена.\nПроверьте написание имени.', icon="✴️")
  else:
    #Загрузка текстовых описаний категорий
    try:
      with open(name, 'r') as file:
        temp_data = file.read()#импорт описаний из файла
      categories = re.findall(r'\b[A-Za-z0-9_]+(?=:)', temp_data.split('\n')[0])
      file_data = temp_data.split('\n')
      DATA = []
      for i in file_data:
          DATA.append(re.findall(r'-?\d+\.\d+', i))
      return pd.DataFrame(DATA, columns = categories).sort_values('Power')
    except:
      st.warning('Ошибка загрузки данных', icon="🟥")
    
#Application part
st.title('Анализ результатов оптимизации')
#Part 1 - Data Loading
st.subheader('Импорт')
st.text('Импорт файла с результатами оптимизации. \nВ поле ниже введите название файла и укажите его расширение (txt/csv/xlsx и др.).')

#Session state settings
#Предусмотрено 3 состояния активной сессии в засисимости от состояния загрузки данных.
#Параметр data_integrity определяется 3 значениями
#0 - Данные не загружены;
#1 - Файл данных существует, но не загружен;
#2 - Файл данных загружен и кэширован.

if 'data_integrity' not in st.session_state:
  #Data not loaded
  st.session_state.data_integrity = 0

c1, c2 = st.columns(2, vertical_alignment="bottom")
FILE_PATH = os.getcwd()+'\\results\\'+c1.text_input(label = 'Файл оптимизации')

c2.button('Проверить файл', on_click=file_check, args=[FILE_PATH])

st.subheader('Данные')
load_button = st.button('Загрузить данные')
if load_button:
  
  DATA = file_load(FILE_PATH)
  st.dataframe(DATA)


      
      

