import pandas as pd

df1 = pd.read_excel(r'C:\Users\Usuario\Desktop\TFG_last\Twitter\df_tw.xlsx')
df2 = pd.read_excel(r'C:\Users\Usuario\Desktop\TFG_last\Facebook\df_fb.xlsx')
df3 = pd.concat(df1,df2)

writer = pd.ExcelWriter(r'C:\Users\Usuario\Desktop\TFG_last\Dashboards\Sentiment analisis.xlsx')
df1.to_excel(writer, 'Twitter')
df2.to_excel(writer, 'Facebook')
df3.to_excel(writer, 'Conjunto')
# Y así sucesivamente para cada archivo

writer.save()
