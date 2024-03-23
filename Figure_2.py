import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Maintenance_Data.csv')
num_features = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
custom_palette = {'L': 'tab:pink', 'M': 'tab:blue', 'H': 'tab:green'}
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(19, 7))
fig.suptitle('Features distribution')
for j, feature in enumerate(num_features):
    sns.kdeplot(ax=axs[j//3, j - 3 * (j//3)], data=df, x=feature, hue='Type', fill=True, palette=custom_palette)

if len(num_features) < 6:
    fig.delaxes(axs.flatten()[-1])

plt.show()
