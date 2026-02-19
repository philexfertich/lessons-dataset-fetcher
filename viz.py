import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns


df = pd.read_csv('units.csv')[['Discipline', 'Section']]
data = df.drop_duplicates(subset=['Section']).groupby('Discipline').size()
print(data)

sns.set_theme(style='white')
palette = sns.color_palette(palette='pastel')

plt.figure(figsize=(6, 6))
plt.pie(data, labels=data.index, colors=palette, autopct='%.0f%%', startangle=90)
plt.title('Disciplines percent ratio')
plt.legend(loc='lower right')
plt.show()