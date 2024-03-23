import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('Maintenance_Data.csv')
def feat_prob(feature, data):
    x, y = [], []
    for j in data[feature].unique():
        temp = data
        temp = temp[temp[feature] >= j]
        y.append(round((temp['Machine failure'].mean()*100), 2))
        x.append(j)
    return(x, y)

plt.figure(figsize=(15, 17))
m = 1
for i in ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']:
    plt.subplot(3, 2, m)
    x, y = feat_prob(i, data)
    plt.xlabel(i)
    plt.ylabel("Possibility of Failure (%)")
    sns.lineplot(y=y, x=x)
    m += 1

plt.tight_layout()
plt.show()
