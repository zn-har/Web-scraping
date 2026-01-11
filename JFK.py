import requests
import csv

BASE_URL = "https://avi-prod-mpp-webapp-api.azurewebsites.net"
AIRPORT = "JFK"

urls = {
    "walktime": f"{BASE_URL}/api/v1/walkTimes/{AIRPORT}",
    "waittime": f"{BASE_URL}/api/CustomClearanceTimesPoints/{AIRPORT}",
    "customs": f"{BASE_URL}/api/CustomClearanceTimesPoints/{AIRPORT}",
}

headers = {
    "Origin": "https://www.jfkairport.com",
    "Referer": "https://www.jfkairport.com/",
}

# Fetch data from API endpoints
response_walktime = requests.get(urls["walktime"], headers=headers)
response_waittime = requests.get(urls["waittime"], headers=headers)

data = response_waittime.json()
print(data)


# with open("airport_walk_times.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#
#     # Header
#     writer.writerow(["terminal_name", "gate_name", "walk_time"])
#
#     # Flatten nested structure
#     for terminal in data["terminals"]:
#         terminal_name = terminal["terminalName"]
#
#         for gate in terminal["gateNames"]:
#             writer.writerow([
#                 terminal_name,
#                 gate["gateName"],
#                 gate["walkTime"],
#             ])
