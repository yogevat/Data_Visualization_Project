import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path = 'Maintenance_Data.csv'
data = pd.read_csv(file_path)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='Type', hue='Machine failure', data=data)
plt.title('Machine Type Distribution with Failure Status')
plt.xlabel('Type')
plt.ylabel('Count')
plt.legend(title='Machine Failure')
plt.show()
