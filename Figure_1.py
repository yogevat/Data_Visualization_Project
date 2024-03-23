import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

file_path = 'Maintenance_Data.csv'
data = pd.read_csv(file_path)

data_subset = data[['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]',
                    'Torque [Nm]', 'Tool wear [min]', 'Machine failure']].sample(n=500, random_state=42)

data_subset = data_subset.rename(columns={
    'Air temperature [K]': 'Air Temp (K)',
    'Process temperature [K]': 'Process Temp (K)',
    'Rotational speed [rpm]': 'Rotate Speed (rpm)',
    'Torque [Nm]': 'Torque (Nm)',
    'Tool wear [min]': 'Tool Wear (min)',
    'Machine failure': 'Machine Failure'
})

scaler = StandardScaler()
numerical_columns = ['Air Temp (K)', 'Process Temp (K)', 'Rotate Speed (rpm)', 'Torque (Nm)', 'Tool Wear (min)']
data_subset[numerical_columns] = scaler.fit_transform(data_subset[numerical_columns])

def scatterplot_diag(x, **kwargs):
    plt.scatter(x, x, **kwargs)

grid = sns.PairGrid(data_subset, hue="Machine Failure", diag_sharey=False)

grid.map_diag(scatterplot_diag, s=10)
grid.map_offdiag(sns.scatterplot, s=10)

grid.add_legend()
plt.show()
plot_filename = 'pairplot_machine_failure.png'
plt.savefig(plot_filename)
plt.close()
