import pandas as pd
import matplotlib.pyplot as plt
import csv

rows = []
with open("failover_log.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    for row in reader:
        if len(row) >= 3:
            timestamp, status, message = row[0], row[1], ",".join(row[2:])
            rows.append([timestamp.strip(), status.strip(), message.strip()])

df = pd.DataFrame(rows, columns=["timestamp", "status", "message"])
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["value"] = df["status"].apply(lambda x: 1 if x == "success" else 0)

plt.figure(figsize=(14, 6))
plt.plot(df["timestamp"], df["value"], marker='o', linestyle='-')
plt.title("Failover Status Over Time (Line Plot)")
plt.xlabel("Timestamp")
plt.ylabel("Status")
plt.yticks([0, 1], ["Error", "Success"])
plt.grid(True)
plt.tight_layout()
plt.savefig("status_timeline.png")
plt.show()