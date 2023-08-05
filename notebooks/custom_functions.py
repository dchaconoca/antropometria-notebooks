#!/usr/bin/env python
# coding: utf-8

# # Estudio grasa corporal y obesidad
# 

# ## Lectura, limpieza, transformación y cálculo
# 
# 1. Leemos el archivo
# 2. Limpiamos y eliminamos los datos erróneos
# 3. Seleccionamos los datos que nos interesan
# 4. Calculamos algunas variables necesarias para el estudio
# 5. Guardamos el resultado en un archivo parquet para la continuación del estudio

# ### Estudio Obesidad
# 
# 1. Clasificación de obesidad según el BMI:
# 
# - Bajo peso (0): BMI < 18.5 
# - Peso normal (1): 18.5 ≤ BMI < 25
# - Sobrepeso (2): 25 ≤ BMI < 30
# - Obesidad (3): BMI ≥ 30
# 
# 2. Clasificación de riesgo de enfermedades no transmisibles y obesidad según la circunferencia de cintura (CC)
# 
# - Si masculino y CC > 94 cm -> Obesidad
# - Si femenino y CC > 80 cm -> Obesidad
# 
# 3. Clasificación de riesgo de enfermedades no transmisibles según el racio circunferencia de cintura y circunferencia de cadera (RCC)
# 
# |Riesgo|Femenino|Masculino|
# |------|---------|--------|
# |Bajo| < 0.8 | < 0.95|
# |Medio|0.81 - 0.85 |0.96 - 1 |
# |Alto| > 0.86| > 1|
# 
# 4. Clasificación de riesgo sobrepeso y riesgo de enfermedades no transmisibles según racio circunferencia cintura y talla (ICT):
# 
# **ESTO LO CAMBIÉ EN EL CÓDIGO PARA DISMINUIR CATEGORÍAS**
# 
# |Riesgo|Femenino|Masculino|
# |------|---------|--------|
# |Muy delgado| < 0.34 | < 0.34|
# |Delgado sano|0.35 - 0.41 |0.35 - 0.42 |
# |Sano| 0.42 - 0.48| 0.43 - 0.52|
# |Sobrepeso| 0.49 - 0.53 | 0.53 - 0.57|
# |Sobrepeso elevado| 0.54 - 0.57| 0.58 a 0.62|
# |Obesidad mórbidad| > 0.58| > 0.63|
# 
# 
# 

# In[1]:


# Librerías

from pathlib import Path

import pandas as pd
import numpy as np

# Armando pipelines
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import FeatureUnion, Pipeline


# In[2]:


def read_file(file, sep=','):
    
    df = pd.DataFrame()
      
    file_type = file[file.index('.') - len(file) + 1:]
       
    if (file_type == 'csv'):
        df = pd.read_csv(file, sep=sep)
    elif (file_type == 'parquet'):
        df = pd.read_parquet(file, engine='fastparquet')
    elif (file_type == 'xlsx' or file_type == 'xls'):
        df = pd.read_excel(file)

    return df


# In[3]:


# Seleccionar solo las columnas necesarias 

def select_data(df, col_drop=[], col_leave=[]):
     
    if col_leave:
        df = df.loc[:,col_leave]
    
    if col_drop:
        df.drop(col_drop, axis=1, inplace=True)
    
    return df


# In[4]:


# Clasificación según BMI: Body Mass Index (Índice de Masa Corporal)

# Cálculo del índice de masa corporal (BMI)
def bmi_calc(weight, height):
    height = height/100
    bmi = weight / (height*height)    
    return bmi

def calc_obesity_bmi(bmi):
    if bmi < 18.5: return 0
    if bmi >= 18.5 and bmi < 25 : return 1
    if bmi >= 25 and bmi < 30 : return 2
    if bmi >= 30 : return 3
    
def calc_obesity_bmi_txt(bmi):
    if bmi == 0: return '0-Bajo Peso'
    if bmi == 1 : return '1-Normal'
    if bmi == 2 : return '2-Sobrepeso'
    if bmi == 3 : return '3-Obesidad'
    


# In[5]:


# Clasificación según CC: Circunferencia de cadera

def calc_obesity_cc(gender, waist_circum):
    if gender=='male':
        if waist_circum>94.0: return 1            
    if gender=='female':
        if waist_circum>80.0: return 1 
    return 0

def calc_obesity_cc_txt(cc):
    if cc == 0: return '0-Bajo'
    if cc == 1 : return '1-Alto'


# In[6]:


# Clasificación según RCC: Racio entre la circunferencia de la cintura y el de la cadera

def calc_obesity_rcc(gender, rcc):

    if gender == 'female':
        if rcc <= 0.8: return 0
        if rcc > 0.8 and rcc <= 0.85 : return 1
        if rcc > 0.85 : return 2
        
    if gender == 'male':
        if rcc <= 0.95: return 0
        if rcc > 0.95 and rcc <= 1 : return 1
        if rcc > 1 : return 2
        
def calc_obesity_rcc_txt(rcc):
    if rcc == 0: return '0-Bajo'
    if rcc == 1: return '1-Medio'
    if rcc == 2: return '2-Alto'
    


# In[7]:


# Clasificación ICT: Índice o racio de circunferencia de cintura y talla (estatura)

def calc_obesity_ict(gender, ict):
    
    if gender == 'female':
        if ict <= 0.41: return 0
        if ict > 0.41 and ict <= 0.48 : return 1
        if ict > 0.48 and ict <= 0.57 : return 2
        if ict > 0.57 : return 3
        
    if gender == 'male':
        if ict <= 0.42: return 0
        if ict > 0.42 and ict <= 0.52 : return 1
        if ict > 0.52 and ict <= 0.62 : return 2
        if ict > 0.62 : return 3
        
def calc_obesity_ict_txt(ict):
    if ict == 0 : return '0-Delgado'
    if ict == 1 : return '1-Normal'
    if ict == 2 : return '2-Sobrepeso'
    if ict == 3 : return '3-Obesidad'
           


# In[8]:


# Cuántos factores de riesgo posee una persona

def calc_risk_factors(bmi, cc, rcc, ict):  
    
    total = 0
    
    if bmi >= 2: total = total + 1
    if cc >= 1: total = total + 1
    if rcc >= 1: total = total + 1
    if ict >= 2: total = total + 1
        
    return total

    


# In[9]:


# Transforma los datos del dataset, 
# en particular pasa las medidas de pulgadas a cm
# y de libras a Kg
# Esta función puede aplicarse a todo el dataset o a un subconjunto del mismo

def custom_transformations(df):
    
    # Columnas que no están en cm
    not_in_cm = ['age', 'age_range', 'gender', 'weight', 'num_children', 'bra_size_chest', 'bra_size_cup', 'shoe_size_us']
    
    # Columnas en cm: Son todas las columnas menos las que se encuentran más arriba
    in_cm_columns = [ele for ele in df.select_dtypes('float64').columns.to_list() if ele not in not_in_cm]
    
    # Transformamos de pulgadas a cm 
    for col in in_cm_columns:
        df[col] = df.apply(lambda  row: row[col] * 2.54, axis=1)
    
    # Transformamos de libras a Kg
    df['weight'] = df.apply(lambda  row: row['weight'] * 0.454, axis=1)

    return df


# In[10]:


# Calcula nuevas variables para el dataset

def custom_calculus(df):
    
    df['gender_bin'] = df.apply(lambda  row: (1 if row['gender']=='male' else 0), axis=1)
    
    # Calculamos el BMI para cada registro
    df['bmi'] = df.apply(lambda  row: bmi_calc(row['weight'], row['height']) , axis=1)

    # Calculamos el racio cintura / cadera para cada registro
    df['rcc'] = df.apply(lambda  row: row['waist_circum_preferred'] / row['hip_circum'], axis=1)
    
    # Calculamos el racio cintura / talla para cada registro
    df['ict'] = df.apply(lambda  row: row['waist_circum_preferred'] / row['height'], axis=1)
    
    df['obesity_bmi'] = df.apply(lambda  row: calc_obesity_bmi(row['bmi']) , axis=1)
    df['obesity_bmi_txt'] = df.apply(lambda  row: calc_obesity_bmi_txt(row['obesity_bmi']) , axis=1)
    
    df['obesity_cc'] = df.apply(lambda  row: calc_obesity_cc(row['gender'], row['waist_circum_preferred']) , 
                                            axis=1)
    df['obesity_cc_txt'] = df.apply(lambda row: calc_obesity_cc_txt(row['obesity_cc']), axis=1)
    
    df['obesity_rcc'] = df.apply(lambda row: calc_obesity_rcc(row['gender'], row['rcc']), axis=1)
    df['obesity_rcc_txt'] = df.apply(lambda row: calc_obesity_rcc_txt(row['obesity_rcc']), axis=1)
    
    
    df['obesity_ict'] = df.apply(lambda row: calc_obesity_ict(row['gender'], row['ict']) , axis=1)
    df['obesity_ict_txt'] = df.apply(lambda row: calc_obesity_ict_txt(row['obesity_ict']) , axis=1)

    
    df['risk_factors'] = df.apply(lambda  row: calc_risk_factors(row['obesity_bmi'], 
                                                                   row['obesity_cc'], 
                                                                   row['obesity_rcc'],
                                                                   row['obesity_ict']) , 
                                            axis=1)
    
    return df

# In[11]:


# Permite hacer transformaciones y cálculos personalizados al subconjunto de datos
# Es un pipeline que llama 2 funciones custom_transformations y custom_calculus

def transform_calcul(df):
    # Aplicamos transformaciones y cálculos personalizados
    custom_transformations_pipeline = Pipeline([
        ('custom_transforms', FunctionTransformer(custom_transformations)), # Función de transformación personalizada
        ('custom_calculus', FunctionTransformer(custom_calculus)) # Función de cálculos personalizados
    ])

    # Aplicar el pipeline al conjunto de datos
    return custom_transformations_pipeline.fit_transform(df)


# In[12]:


# Esta función puede ser utilizada para extraer un subconjunto de datos del dataset original
# Parámetros:
#   columns_to_drop: Lista de columnas que se quiere borrar (cuando se desea conservar la mayoría)
#   columns_to_leave: Lista de columnas que se quiere conservar
#   transform: Boolean que indica si se va o no ejecutar la función transform_calculEs

def load_clean_transform(columns_to_drop, columns_to_leave, transform=True):
    
    # Leemos el archivo
    CURRENT_DIR = Path.cwd()
    
    BASE_DIR = Path(CURRENT_DIR).parent

    file = f"{BASE_DIR}/data/in/caesar.csv"

    df = read_file(file, ',')

    # Limpiamos y eliminamos los datos erróneos
    
    # Borramos la primera línea que no contiene datos significativos
    df.drop([0], axis=0, inplace=True)
    
    # Seleccionamos las variables que nos interesan
    # Esta función debería hacer un select en la BD para traer lo que nos interesa
    # según el problema que estamos tratando
    df = select_data(df, columns_to_drop, columns_to_leave)

    # Si la cantidad de registros con valores nulos es menos de 1% los eliminamos
    nul_vals = df[ df.isnull().values ]['gender'].count() / df['gender'].count()

    if nul_vals <= 0.01: df.dropna(inplace=True)
        
    if transform:
        df = transform_calcul(df)
    
    # Guardamos el resultado en un archivo parquet para el resto del estudio
    
    df.to_parquet(f"{BASE_DIR}/data/out/obesity.parquet", 
                    compression='GZIP',
                    engine='pyarrow')
    
    return df


# ## Main

# In[13]:


columns_to_drop = []
columns_to_leave = [
 'age',
 'age_range',
 'gender',
 'height',
 'weight',
 'waist_circum_preferred',
 'hip_circum'
]

df_obesity = load_clean_transform(columns_to_drop, columns_to_leave, True)


# In[14]:


df_obesity


# In[15]:


df_obesity.info()


# In[16]:


df_obesity.describe()





