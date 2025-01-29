import matplotlib.pyplot as plt
import pandas as pd

# The data as output from the sparql query into a DataFrame
data = {
    "districtName": ["Bergedorf", "Wandsbek", "Harburg", "Eimsbüttel", "Altona", "Hamburg-Nord", "Hamburg-Mitte"],
    "migrationPercentage": [42.4, 37.6, 52.7, 33.1, 36.5, 32.9, 54.9],
    "busStopsPerThousand": [2.779999, 0.9183079, 1.4643689, 0.6625106, 0.9898945, 0.72156227, 1.5321088],
}
df = pd.DataFrame(data)

# Build the Figure with malplotlib
plt.figure(figsize=(10, 6))
plt.scatter(df['migrationPercentage'], df['busStopsPerThousand'], color='yellow', alpha=0.7)
for i, row in df.iterrows():
    plt.text(row['migrationPercentage'], row['busStopsPerThousand'], row['districtName'], fontsize=9)
# Write the labels. There is no need for a title
plt.xlabel('Migration Percentage')
plt.ylabel('Bus Stops per 1000')
plt.title('')
plt.grid(alpha=0.5)

# Safe it as a file for use in report
plt.savefig('migrants_vs_bus_stops.png', format='png', dpi=300, bbox_inches='tight')
print("Diagram saved")