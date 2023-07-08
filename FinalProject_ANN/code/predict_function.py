import torch
import torch.nn as nn

import requests
import json
import numpy as np
import pandas as pd

url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'

def process_data():
    # Read JSON
    response = requests.get(url)
    data = json.loads(response.text)

    # Deal data
    filtered_data = []
    ar = []
    total = []
    for d in data:
        address = d.get('ar')
        tot = d.get('tot')
        sno = d.get('sno')
        sbi = d.get('sbi')
        if sbi is not None and sno != '500113069':
            filtered_data.append(sbi)
            ar.append(address)
            total.append(tot)

    return filtered_data, ar, total

# define the model
class MyModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(MyModel, self).__init__()
        self.model = nn.Sequential(
                nn.Linear(input_dim, 512),
                nn.ReLU(),
                nn.Dropout(0.5), 
                nn.Linear(512, 512),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(512, output_dim)
            )

    def forward(self, x):
        out = self.model(x)
        return out

def predict(input_data):
    input_dim = 1279 
    output_dim = 1279
    model = MyModel(input_dim, output_dim)

    # load the model.pt
    model.load_state_dict(torch.load('NN_project/model.pt', map_location=torch.device('cpu')))
    model.eval()

    # predict
    with torch.no_grad():
        input_tensor = input_data.to(torch.float32) 
        output = model(input_tensor).to(torch.int8)

    return output.tolist()[0]


# function: get infomation
def get_info():
    filtered_data, ar, tot = process_data()

    # convert the data into torch, torch shape is (1, 1279)
    data_tensor = torch.stack([torch.tensor(d) for d in filtered_data])
    data_tensor = data_tensor.unsqueeze(0)  

    # predict
    prediction = predict(data_tensor.to(torch.float32))
    return ar, filtered_data, prediction, tot
