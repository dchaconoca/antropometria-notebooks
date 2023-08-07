# # Estudio de las Medidas Antropométricas para determinar el riesgo de obesidad y ENT

>Autora: Diana Chacón Ocariz


##  Estudio del sobrepeso y la obesidad y su incidencia en las ENT:

La obesidad y el sobrepeso son condiciones de salud que han alcanzado proporciones epidémicas a nivel mundial, siendo un factor determinante en el desarrollo de diversas enfermedades no transmisibles (ENT). Estas condiciones se caracterizan por un exceso de grasa corporal, lo que puede tener consecuencias significativas para la salud a largo plazo.

El sobrepeso y la obesidad aumentan sustancialmente el riesgo de padecer enfermedades crónicas, como la diabetes tipo 2, la hipertensión y las enfermedades cardiovasculares. Estas afecciones pueden tener un impacto negativo en la calidad de vida, aumentando la morbilidad y la mortalidad en las poblaciones afectadas.

Para evaluar y cuantificar el grado de sobrepeso y obesidad, se utilizan medidas antropométricas clave:

1. **Índice de Masa Corporal (IMC):** Relaciona el peso y la altura de una persona. Sin embargo, es importante señalar que el IMC no distingue entre masa muscular y grasa, por lo que puede haber limitaciones en su interpretación, especialmente en atletas o personas con una distribución de grasa atípica.

2. **Relación cintura-cadera (RCC) y la relación cintura-talla (RCT):** Estos indicadores ofrecen una perspectiva más completa sobre la distribución de la grasa corporal. Una acumulación excesiva de grasa en la región abdominal, medida mediante el **contorno de cintura**, está particularmente asociada con un mayor riesgo de enfermedades metabólicas y cardiovasculares. Un contorno de cintura elevado puede indicar la presencia de grasa visceral, que se asocia con inflamación y otros procesos patológicos.

3. **La edad y el sexo:** A medida que las personas envejecen, es común experimentar cambios en el metabolismo y en la composición corporal, lo que puede influir en la tendencia a ganar peso. Además, existe evidencia de que las tasas de obesidad varían según el género, con diferencias en la distribución de grasa y en las respuestas hormonales.

**Sin embargo, no existe una fórmula que combine todos estos datos y nos permita saber de manera objetiva el riesgo que tiene una persona de padecer obesidad y ENT.**

## Definición del problema y objetivo del estudio:

**Determinar, a partir de medidas antropométricas, el grado de riesgo que corre una persona de padecer obesidad y/o ENT.** 

Se trata de determinar la variable **obesity** que indica 3 grados de riesgo:

1. Riesgo bajo o nulo (0)
2. Riesgo medio (1)
3. Riesgo alto (2)

a partir de la edad, el género, el peso, la estatura, el contorno de cintura y el contorno de cadera de una persona.

La variable objetivo no se encuentra dentro del conjunto de datos. 

Con los datos existentes, es posible calcular indicadores definidos más arriba y que permiten determinar el grado de riesgo. Sin embargo, no existe una fórmula o algún criterio objetivo que permita calcular el riesgo tomando en cuenta todas estas medidas.

El objetivo es usar modelos de ML para:

1. Identificar grupos de personas con características similares (clasificación no supervisada) y poderlas etiquetar (asignación manual de la variable objetivo).
2. A partir de los datos etiquetados, entrenar un modelo de clasificación supervisada que permita predecir el grado de riesgo.
    
    
## Fuente de los datos:

#### Fuente principal:

Existen muchos datasets de datos antropométricos. Sin embargo, este me pareció el más pertinente por la cantidad y variedad de la información:

https://www.kaggle.com/datasets/thedevastator/3-d-anthropometry-measurements-of-human-body-sur?select=caesar.csv

**Créditos:** Andy R. Terrel: https://data.world/andy

#### Subconjunto de datos utilizados en el estudio:

- **age:**  Edad
- **age_range:**  Rango de edad. Variable categórica
- **gender:**  Sexo (male, female). Variable categórica
- **height:**  Altura (en pulgadas)
- **hip_circum:**  Contorno de cadera (en pulgadas)
- **weight:**  Peso (en libras)
- **waist_circum_preferred:**  Contorno de cintura (en pulgadas)

Aquí una descripción completa del dataset: [Metadatos](https://github.com/dchaconoca/antropometria-notebooks/blob/61f5aa8bf92dce0f3d48a3fd3853d57992d6ba90/notebooks/Metadatos.ipynb)

## Enfoque técnico para la realización del estudio:

Pasos generales que seguí para llevar a cabo el estudio:

    - Buscar y seleccionar un subconjunto de datos o medidas antropométricas pertinentes para el estudio.
    - Calcular indicadores que permiten determinar el riesgo de padecer obecidad o ENT.
    - Utilizar modelos de clasificación no supervisada para encontrar grupos y así etiquetar los datos.
    - Seleccionar el mejor modelo de ML para predecir el riesgo de que una persona pueda sufrir de obesidad o ENT
    - Implementar un prototipo de aplicación que permita a cualquier persona, conocer el grado de riesgo de padecer obesidad o ENT.


## Notebooks del Estudio:

1. [NB1: Lectura, limpieza, transformación y cálculo de nuevas variables](https://github.com/dchaconoca/antropometria-notebooks/blob/b002232e5f476a3536d7ead00225f1d376edc010/notebooks/01-obesity-load.ipynb): Carga, limpieza y transformación de los datos. Cálculo de nuevas variables necesarias al estudio. Almacenamiento de los datos en archivo .parquet para el resto del estudio.
1. [NB2: EDA y Visualización de los Datos](https://github.com/dchaconoca/antropometria-notebooks/blob/b002232e5f476a3536d7ead00225f1d376edc010/notebooks/02-obesity-eda.ipynb): Exploración y análisis de los datos.
1. [NB3: Clasificación no supervisada y etiquetado de los datos](https://github.com/dchaconoca/antropometria-notebooks/blob/b002232e5f476a3536d7ead00225f1d376edc010/notebooks/03-obesity-eda-clusters.ipynb): Clasificación y etiquetado de los datos. Análisis de los clusters. Análisis de la etiqueta.
1. [NB4: Entrenamiento del modelo](https://github.com/dchaconoca/antropometria-notebooks/blob/b002232e5f476a3536d7ead00225f1d376edc010/notebooks/04-obesity-train-model.ipynb): Escogencia del modelo. Ajuste del modelo. Salvaguarda del modelo entrenado. Predicciones.


[Repostitorio GitHub](https://github.com/dchaconoca/antropometria-notebooks.git)

## Implementación del prototipo de la aplicación:

A partir de los datos que el usuario introduce, la aplicación (hecha utilizando Streamlit) consulta una API (desarrollada con FastAPI) que carga el modelo de ML entrenado, y devuelve:

1. Indicadores y sus índices de riesgo: Índice de masa corporal, contorno de cintura, racio entre cintura y cadera, racio entre cintura y estatura.
2. Ińdice de riesgo predicho por el modelo: Riesgo bajo o nulo, riesgo medio, riesgo alto.

#### [dIAna antropometría y obesidad](https://diana-antropometria.streamlit.app/)

[Repostitorio GitHub](https://github.com/dchaconoca/antropometria-app)

**Nota:** Los resultados NO deben tomarse como la opinión de un especialista. Esto es un simple ejercicio de ciencia de datos.


![Prototipo-dIAna.png](attachment:Prototipo-dIAna.png)


## Instrucciones para la ejecución del proyecto:

Ejecutar los workflows definidos al final de los notebooks en el siguiente orden:

**Para limpiar, transformar, etiquetar los datos y entrenar el modelo:

1. **NB-01:** Función **load_clean_transform**
2. **NB-03:** Función **label_data**
3. **NB-04:** Función **save_model**

**Para hacer predicciones:**

1. **NB-04:** Función **make_obesity_prediction**

También es posible probar la implementación de la aplicación:

### Probar la aplicación [dIAna antropometría y obesidad](https://diana-antropometria.streamlit.app/)
    