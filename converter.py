import pandas as pd
import ast
import numpy as np

df = pd.read_csv("raw_airport_data.csv")

output = []

for _, row in df.iterrows():
    airport = row["airport"]
    data_type = row["data_type"]
    ts = row["timestamp"]

    try:
        data = ast.literal_eval(row["details"])
    except:
        continue

    if airport == "Heathrow":
        if "Security" in data_type:
            max_vals = []
            for q in data:
                for m in q["queueMeasurements"]:
                    if m["name"] == "maximumWaitTime":
                        max_vals.append(m["value"])
            if max_vals:
                output.append(("LHR", "security", max(max_vals), ts))

        if "Immigration" in data_type:
            max_vals = []
            for q in data:
                for m in q["queueMeasurements"]:
                    if m["name"] == "maximumWaitTime":
                        max_vals.append(m["value"])
            if max_vals:
                output.append(("LHR", "customs", max(max_vals), ts))

    if airport == "JFK" and data_type == "Wait Times":
        for q in data:
            output.append(("JFK", "security", q["timeInMinutes"], ts))

    if airport == "JFK" and data_type == "Walk Times":
        times = []
        for term in data["terminals"]:
            for g in term["gateNames"]:
                lo, hi = g["walkTime"].split("-")
                times.append((int(lo) + int(hi)) / 2)
        if times:
            output.append(("JFK", "walk", np.mean(times), ts))


summary = {}

for airport, ttype, value, ts in output:
    if airport not in summary:
        summary[airport] = {"security": None, "customs": None, "walk": None, "ts": ts}

    summary[airport][ttype] = round(value, 1)
    summary[airport]["ts"] = ts

rows = []
for airport, v in summary.items():
    rows.append([
        airport,
        v["security"],
        v["customs"],
        v["walk"],
        v["ts"]
    ])

dashboard = pd.DataFrame(rows, columns=[
    "Airport",
    "Security Wait (min)",
    "Customs Wait (min)",
    "Walk to Gates (min)",
    "Timestamp"
])

dashboard.to_csv("airport_dashboard.csv", index=False)
print(dashboard)
