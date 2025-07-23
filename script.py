import pandas as pd
import json

df = pd.read_excel("C:/Users/plenarcik/Downloads/spread python.xlsx", header=None)

output = []

for index, row in df.iterrows():
    alias = str(row[0])
    max_spread_value = (
            if float(row[4]) = int



    entry = {
        "aliasNames": [alias],
        "configuration": {
            "decimalPlaces": 3,
            "maxSpreadAction": "CHANGE_SPREAD",
            "maxSpread": max_spread_value
        }
    }
    output.append(entry)


print(json.dumps(output, indent=2))
