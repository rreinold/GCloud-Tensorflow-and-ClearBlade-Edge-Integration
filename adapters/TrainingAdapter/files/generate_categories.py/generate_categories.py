import pandas as pd
import json
import base64
import ast
import requests

def convert_to_float(df, arr):
    for i in arr:
        df[i] = df[i].astype('float32')

    numeric_columns = df.select_dtypes(['int64','float32','float64']).columns
    df[numeric_columns] = df[numeric_columns].astype('float32')
    return df

def create_categorical_mapping(df):
    cat_columns = df.select_dtypes(['object']).columns
    _CATEGORICAL_TYPES = {}
    for col in cat_columns:
        _CATEGORICAL_TYPES[col] = pd.api.types.CategoricalDtype(categories=df[col].unique())

    cat_data = {}
    for i in cat_columns:
        opt = list(_CATEGORICAL_TYPES[i].categories)
        cat_data[i] = dict(zip(opt, list(range(0,len(opt)))))

    with open("categorical_data.json", 'w') as cd:
        json.dump(cat_data, cd)

    return df, cat_data

def create_mean_std_mapping(df, label):
    prediction = df.pop(label)
    meanstd = {}
    dtypes = list(zip(df.dtypes.index, map(str, df.dtypes)))
    for column, dtype in dtypes:
        if dtype == 'float32' or dtype == 'float64':
            meanstd[column] = {"mean":float(df[column].mean()), "std":float(df[column].std())}

    with open("meanstd_data.json", 'w') as ms:
        json.dump(meanstd, ms)

    return meanstd

def send_data_to_collections(cat_data, meanstd, to_clean, label, token):
    cat_data = str(cat_data)
    cat_data = cat_data.encode()
    encoded_cat = base64.b64encode(cat_data).decode('ascii')

    meanstd = str(meanstd)
    meanstd = meanstd.encode()
    encoded_meanstd = base64.b64encode(meanstd).decode('ascii')

    to_clean = str(to_clean)
    to_clean = to_clean.encode()
    encoded_to_clean = base64.b64encode(to_clean).decode('ascii')
    
    header = {
        "ClearBlade-UserToken" : token,
        "collectionID" : "96f5ced30bf4d89ec0e4db91f668"
    }

    body = {
        "categorization" : encoded_cat,
        "normalization" : encoded_meanstd,
        "to_clean_data" : encoded_to_clean,
        "prediction_label" : label
    }

    response = requests.post("https://staging.clearblade.com/api/v/1/data/96f5ced30bf4d89ec0e4db91f668", headers=header, data=json.dumps(body))

    return response.status_code
    # decoded_cat = base64.b64decode(encoded_cat)
    # decoded_cat = decoded_cat.decode('ascii')
    # decoded_cat = ast.literal_eval(decoded_cat)
    # print(decoded_cat)
    # print(type(decoded_cat))

def main():
    with open("train_params.json",'r') as fp:
        train_params = json.load(fp)

    collection = train_params["featureCol"] + ".json"
    label = train_params["label"]
    to_clean = train_params["toClean"]
    token = train_params["usertoken"]

    with open(collection, 'r') as cl:
        data = json.load(cl)
        df = pd.DataFrame(data=data)

    item_id = df.pop("item_id")

    return df, label, to_clean, token

arr = ['price','horsepower','normalized_losses','peak_rpm','bore','stroke']
df, label, to_clean, token = main()
df = convert_to_float(df, arr)
df, cat_data = create_categorical_mapping(df)
meanstd = create_mean_std_mapping(df, label)
status_code = send_data_to_collections(cat_data, meanstd, to_clean, label, token)
print(status_code)