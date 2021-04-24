import pandas as pd
import colorsys
from scipy.spatial.distance import cdist
import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from apyori import apriori
import csv
color = pd.read_csv("movie.csv")
x11 = pd.read_csv("x11.csv")
# color = data.iloc[:, 1:]


def to_rgb(hex):
    """Conver hex to rgb"""
    # print(hex)
    hex = hex.lstrip("#")
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hsv(rgb):
    """Convert rgb to hsv"""
    r, g, b = rgb
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    v = mx * 100
    return (round(h, 2), round(s, 2), round(v, 2))

def closest_point(value, df):
    """ Find closest point from a list of points. """
    return df[cdist([value], df).argmin()]

def match_value(df, col1, x, col2):
    """ Match value x from col1 row to value in col2. """
    return df[df[col1] == x][col2].values[0]

def to_int(hex):
    hex = hex.lstrip("#")
    return int(hex, 16)

# def to_hex(int):
    


# convert hex to rgb
color['Dominant1'] = color.apply(lambda x: to_rgb(x['Dominant1']), axis=1)
color['Dominant2'] = color.apply(lambda x: to_rgb(x['Dominant2']), axis=1)
color['Dominant3'] = color.apply(lambda x: to_rgb(x['Dominant3']), axis=1)



# # convert rgb to hsv
color['Dominant1'] = color.apply(lambda x: rgb_to_hsv(x['Dominant1']), axis=1)
color['Dominant2'] = color.apply(lambda x: rgb_to_hsv(x['Dominant2']), axis=1)
color['Dominant3'] = color.apply(lambda x: rgb_to_hsv(x['Dominant3']), axis=1)



x11["hsv"] = list(
    zip(
        x11["Hue (HSL/HSV)"].str[:-1].astype(float),
        x11["Satur. (HSV)"].str[:-1].astype(float),
        x11["Value"].str[:-1].astype(float),
    )
)

# normalize the value
color['Dominant1'] = [closest_point(x, list(x11['hsv'])) for x in color['Dominant1']]
color['Dominant1'] = [match_value(x11, 'hsv', x, 'Name') for x in color['Dominant1']]

color['Dominant2'] = [closest_point(x, list(x11['hsv'])) for x in color['Dominant2']]
color['Dominant2'] = [match_value(x11, 'hsv', x, 'Name') for x in color['Dominant2']]

color['Dominant3'] = [closest_point(x, list(x11['hsv'])) for x in color['Dominant3']]
color['Dominant3'] = [match_value(x11, 'hsv', x, 'Name') for x in color['Dominant3']]


color.to_csv('output.csv')




# ASSOCIATE MINING

# DROP COLOR PALLET FROM TABLE
col_list=["Dominant1","Dominant2","Dominant3"]
data=pd.read_csv("output.csv",usecols=col_list)
records = []
with open("output.csv") as csvfile:
    reader = csv.reader(csvfile,quotechar='|') # change contents to floats
    for row in reader: # each row is a list
        records.append(row)
# print(records)
# caculate 
check=list(apriori(records,min_support=0.01))
DF = pd.DataFrame(check)
DF.to_csv("data1.csv")

table=pd.read_csv("data1.csv")
for i in range(0,len(table["items"])):
    table["items"][i]=frozenset[0]
# association_rules = apriori(records, min_support=0.00000001, min_confidence=0.00000001, min_lift=0.0000001, min_length=2)
# association_results = list(association_rules)
# print(association_results)
# # for item in association_results:
# #     # print(item)
# #     # print('\n')    
# #     # first index of the inner list
# #     # Contains base item and add item
# #     pair = item[0] 
# #     items = [x for x in pair]
# #     a="Support: "

# #     for idx in range(1,len(item[0])):
# #         a=a+str(items[idx])
# #     #second index of the inner list
# #     print(a)
# #     #third index of the list located at 0th
# #     #of the third index of the inner list

# #     print("Confidence: " + str(item[2][0][2]))
# #     print("Lift: " + str(item[2][0][3]))