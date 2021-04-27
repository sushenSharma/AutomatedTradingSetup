from collections import Counter

import pandas as pd
data = pd.read_csv("Actual_result_daily.csv")

Sector_Series = data["Sector"].to_list()
print(type(Sector_Series))



j =  [[x,Sector_Series.count(x)] for x in set(Sector_Series)]
print(j)