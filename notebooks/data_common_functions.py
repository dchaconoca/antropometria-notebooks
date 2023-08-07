#################################
## Common Functions
#################################

# Transform columns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler, LabelBinarizer, OrdinalEncoder
from sklearn.compose import ColumnTransformer

# Pipelines
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion, Pipeline

from pathlib import Path

import pandas as pd


#################################

# Read a file according to type

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



# Select columns of a dataframe
# Returns a dataset only with the selected columns

def select_data(df, col_drop=[], col_leave=[]):
     
    if col_leave:
        df = df.loc[:,col_leave]
    
    if col_drop:
        df.drop(col_drop, axis=1, inplace=True)
    
    return df


# Crea y transforma el DF para utilizar el algoritmo KMeans
# con las variables: age_range, gender, height, weight, waist_circum_preferred y hip_circum
def transform_df(df, columns_to_encode, columns_to_scale, columns_to_pass):
    
    CURRENT_DIR = Path.cwd()
    BASE_DIR = Path(CURRENT_DIR).parent
    
    ordinal_cols = ( ['age_range'] if 'age_range' in columns_to_encode else [] )
    columns_to_encode = ( ['gender'] if 'gender' in columns_to_encode else [] )
    
    ordinal_encoding = ColumnTransformer([
        (
            'ordinal_encoding',
            OrdinalEncoder(categories=[['17-25', '26-35', '36-45', '46-55', '56-65', '66-100']]),
            ordinal_cols
        )
    ])
    
    label_binarizer_encoding = ColumnTransformer([
        (
            'label_binarizer_encode',
            #OneHotEncoder(sparse_output=False, handle_unknown="ignore"),
            LabelBinarizer(),
            columns_to_encode
        )
    ])
    
 
    internal_standard_scaler = StandardScaler()

    standard_scaler = ColumnTransformer([
        (
            'standard_scaler',
            internal_standard_scaler,
            columns_to_scale
        )
    ])
    
    passthrough = ColumnTransformer([
        (
            "pass_columns",
            "passthrough",
            columns_to_pass
        )
    ])
    
    feature_engineering_pipeline = Pipeline(
    [
        (
            "features",
            FeatureUnion(
                [
                    ("label_binarizer_encode", label_binarizer_encoding),
                    #("ordinal_encode", ordinal_encoding),
                    ("standard_scaler", standard_scaler),
                    ('passthrough', passthrough)
                ]
            ),
        )
    ])
    
    #feature_engineering_pipeline.fit(df)
    
    #with open(f"{BASE_DIR}/models/feature_engineering_pipeline.pkl", "wb") as f:
    #        pickle.dump(feature_engineering_pipeline, f)
    
    result = feature_engineering_pipeline.fit_transform(df) 
    
    print(result)
    
    return result
    

