from typing import Dict
from pandas_datareader import data
import pandas as pd
import os.path
import os
from tqdm import tqdm
panel:Dict[str, pd.DataFrame] = {}

# for fileName in tqdm(os.listdir("data")):
#     panel[fileName.replace(".csv","")] = pd.read_csv(f"data/{fileName}", sep=',', header = 0)

# count = 0
# for key in tqdm(panel.keys()):
#     count+=len(panel[key])
# print(count)
# exit()
for stock in tqdm(open("allTickers.txt","r").read().split("\n")):
    try:
        data.DataReader(stock, "yahoo", start="1980-01-01").to_csv(f"data/{stock}.csv", sep=',')
    except Exception as e:
        print(e)
        print(f"Could not download:{stock}\n")
    
