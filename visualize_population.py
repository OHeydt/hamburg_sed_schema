import matplotlib.pyplot as plt
import pandas as pd

# The data as output from the sparql query into a DataFrame
data = {
    "districtName": ["Wandsbek", "Hamburg-Nord", "Hamburg-Mitte", "Altona", "Eimsbüttel", "Harburg", "Bergedorf"],
    "population": [455185, 328454, 312641, 280838, 276222, 176868, 133813],
    "numBusStops": [418, 237, 479, 278, 183, 259, 372],
}
df = pd.DataFrame(data)

# Build the Figure with malplotlib
plt.figure(figsize=(10, 6))
plt.scatter(df['population'], df['numBusStops'], color='yellow', alpha=0.7)
for i, row in df.iterrows():
    plt.text(row['population'], row['numBusStops'], row['districtName'], fontsize=9, ha='right')
# Write the labels. There is no need for a title
plt.xlabel('Population')
plt.ylabel('Number of Bus Stops')
plt.title('')
plt.grid(alpha=0.5)

# Safe it as a file for use in report
plt.savefig('population_vs_bus_stops.png', format='png', dpi=300, bbox_inches='tight')
print("Diagram saved")