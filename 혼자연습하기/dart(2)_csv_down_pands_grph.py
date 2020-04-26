import os
import pandas as pd
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width', 1000)

# df_sample = pd.DataFrame([[4,2,3],[9,1,5]])
# print(df_sample)

d = {}
for filename in os.listdir():
    if filename[-3:] == 'csv' :
        df = pd.read_csv(f'./{filename}' , encoding='euc-kr')
        df_boolean = df == '당기순이익(손실)'
        y = df_boolean.sum(axis=0).values.argmax()
        x = df_boolean.sum(axis=1).values.argmax()
        num = df.iloc[x, y + 1]
        d[filename[7:14]] = int(num)

import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()