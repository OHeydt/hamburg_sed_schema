import matplotlib.pyplot as plt
import pandas as pd

# The data as output from the sparql query into a DataFrame
data = {
    "districtName": ["Wandsbek", "Hamburg-Nord", "Hamburg-Mitte", "Altona", "Eimsbüttel", "Harburg", "Bergedorf"],
    "carsPerThousand": [383, 300, 252, 321, 323, 328, 386],
    "busStopsPerThousand": [0.9183079, 0.72156227, 1.5321088, 0.9898945, 0.6625106, 1.4643689, 2.779999],
}
df = pd.DataFrame(data)

# Build the Figure with malplotlib
plt.figure(figsize=(10, 6))
plt.scatter(df['carsPerThousand'], df['busStopsPerThousand'], color='yellow', alpha=0.7)
for i, row in df.iterrows():
    plt.text(row['carsPerThousand'], row['busStopsPerThousand'], row['districtName'], fontsize=9, ha='right')
# Write the labels. There is no need for a title
plt.xlabel('Cars per 1000 People')
plt.ylabel('Bus Stops per 1000 People')
plt.title('')
plt.grid(alpha=0.5)

# Safe it as a file for use in report
plt.savefig('cars_vs_bus_stops.png', format='png', dpi=300, bbox_inches='tight')
print("Diagram saved")