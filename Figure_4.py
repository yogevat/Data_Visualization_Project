import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull
import matplotlib.patches as mpatches
from matplotlib.collections import PathCollection
import matplotlib.patheffects as PathEffects
import plotly.express as px

file_path = 'Maintenance_Data.csv'
data = pd.read_csv(file_path)

def determine_error_type(row):
    error_types = {'TWF': 'Tool Wear Failure', 'HDF': 'Heat Dissipation Failure',
                   'PWF': 'Power Failure', 'OSF': 'Overstrain Failure', 'RNF': 'Random Failure'}
    errors = [error_types[error] for error in error_types if row[error] == 1]
    return ', '.join(errors) if errors else 'No Failure'


data['Error Type'] = data.apply(determine_error_type, axis=1)

# Power (in watts) = Torque (Nm) * RPM * 2 * pi / 60
data['Power [W]'] = data['Torque [Nm]'] * data['Rotational speed [rpm]'] * 2 * np.pi / 60

data_with_failure = data[data['Error Type'] != 'No Failure']
error_columns = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
data_errors = data_with_failure[error_columns]
melted_data = data_with_failure.melt(id_vars=['Power [W]', 'Process temperature [K]'], value_vars=error_columns,
                                     var_name='Error Type', value_name='Error Occurrence')

melted_data = melted_data[melted_data['Error Occurrence'] == 1]
plt.figure(figsize=(10, 8))
scatter_plot = sns.scatterplot(data=melted_data, x='Power [W]', y='Process temperature [K]',
                               hue='Error Type', marker='o', palette='deep')
plt.title('Shir and Daniel Love Forever')
plt.xlabel('Power (Watts)')
plt.ylabel('Process Temperature [K]')

for error_type in melted_data['Error Type'].unique():
    subset = melted_data[melted_data['Error Type'] == error_type]
    kmeans = KMeans(n_clusters=1).fit(subset[['Power [W]', 'Process temperature [K]']])
    centroid = kmeans.cluster_centers_[0]
    if len(subset) >= 3:
        hull = ConvexHull(subset[['Power [W]', 'Process temperature [K]']])
        poly = plt.Polygon(subset[['Power [W]', 'Process temperature [K]']].iloc[hull.vertices],
                           alpha=0.3, color=scatter_plot.get_legend().legendHandles[
                melted_data['Error Type'].unique().tolist().index(error_type)].get_facecolor())
        plt.gca().add_patch(poly)

        text = plt.text(centroid[0], centroid[1], error_type, ha='center', va='center', color='black', fontsize=10)
        text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])


handles, labels = scatter_plot.get_legend_handles_labels()
new_handles = [mpatches.Patch(color=handle.get_facecolor()[0]) for handle in handles]
plt.legend(handles=new_handles, labels=labels, title="Error Type")


# Make the legend interactive
def on_pick(event):
    legpatch = event.artist
    isVisible = legpatch.get_visible()
    legpatch.set_visible(not isVisible)

    error_type = legpatch.get_label()
    for lh in scatter_plot.collections:
        if isinstance(lh, PathCollection) and lh.get_label() == error_type:
            lh.set_visible(not isVisible)
    for ph in plt.gca().get_children():
        if isinstance(ph, mpatches.Polygon) and ph.get_label() == error_type:
            ph.set_visible(not isVisible)
    plt.draw()


# plt.gcf().canvas.mpl_connect('pick_event', on_pick)
fig = px.scatter(melted_data, x='Power [W]', y='Process temperature [K]',
                 color='Error Type', title='Dynamics of Machine Performance: Power, Temperature, and Error Analysis')

# Update layout for a better appearance
fig.update_layout(legend_title_text='Error Type')
fig.update_traces(marker=dict(size=10))

# Show the plot
fig.show()
# plt.show()
