import pandas as pd

df = pd.read_excel('/Users/magdalena/PycharmProjects/rice/birth_death/results/T=260/stats/4-N-443-mu-occur.xlsx', dtype=str)
df = df.set_index(keys=['Unnamed: 0'])

# df = pd.read_csv('/Users/magdalena/Documents/PhD/RU/sortowanie/For_Magda_Anonymous/Batch4_Sim4A.csv', index_col=0)

# df.drop(columns=['Row', 'Marker', 'hclust_index'], inplace=True)
# df.drop(index=1, inplace=True)
# df = df.transpose()
df = df.replace('0', 'A')
df = df.replace('1', 'T')

sequence = ''
for index in df.index:
    sequence += f'>{index}\n'
    sequence += f'{"".join(list(df.loc[index]))}\n'

with open('/birth_death/results/T=260/stats/4-N-443-mutations-AT.txt', 'w') as file:
    file.write(sequence)
