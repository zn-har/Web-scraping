import requests
import csv
from datetime import datetime
HEATHROW_BASE_URL = "https://api-dp-prod.dp.heathrow.com/pihub"
HEATHROW_HEADERS = {
    "Origin": "https://www.heathrow.com",
    "Referer": "https://www.heathrow.com/",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
}

heathrow_urls = {
    "security": f"{HEATHROW_BASE_URL}/securitywaittime?checkpointFacilityType=securityStandard",
    "immigration": f"{HEATHROW_BASE_URL}/immigrationwaittime/ByTerminal",
}

JFK_BASE_URL = "https://avi-prod-mpp-webapp-api.azurewebsites.net"
JFK_HEADERS = {
    "Origin": "https://www.jfkairport.com",
    "Referer": "https://www.jfkairport.com/",
}

jfk_urls = {
    "walktime": f"{JFK_BASE_URL}/api/v1/walkTimes/JFK",
    "waittime": f"{JFK_BASE_URL}/api/CustomClearanceTimesPoints/JFK",
}


def fetch_heathrow_data():
    """Fetch Heathrow security and immigration wait times."""
    print("Fetching Heathrow data...")
    data = {"airport": "Heathrow", "timestamp": datetime.now().isoformat()}
    
    try:
        response = requests.get(heathrow_urls["security"], headers=HEATHROW_HEADERS)
        print(f"  Security wait time status: {response.status_code}")
        if response.status_code == 200:
            data["security"] = response.json()
    except Exception as e:
        print(f"  Error fetching security data: {e}")
    
    try:
        for terminal in range(2, 6):
            immigration_url = f"{heathrow_urls['immigration']}/{terminal}"
            response = requests.get(immigration_url, headers=HEATHROW_HEADERS)
            print(f"  Terminal {terminal} immigration status: {response.status_code}")
            if response.status_code == 200:
                if "immigration" not in data:
                    data["immigration"] = {}
                data["immigration"][f"terminal_{terminal}"] = response.json()
    except Exception as e:
        print(f"  Error fetching immigration data: {e}")
    
    return data


def fetch_jfk_data():
    """Fetch JFK walk times and wait times."""
    print("Fetching JFK data...")
    data = {"airport": "JFK", "timestamp": datetime.now().isoformat()}
    
    try:
        response_walktime = requests.get(jfk_urls["walktime"], headers=JFK_HEADERS)
        print(f"  Walk time status: {response_walktime.status_code}")
        if response_walktime.status_code == 200:
            data["walktime"] = response_walktime.json()
    except Exception as e:
        print(f"  Error fetching walk time data: {e}")
    
    try:
        response_waittime = requests.get(jfk_urls["waittime"], headers=JFK_HEADERS)
        print(f"  Wait time status: {response_waittime.status_code}")
        if response_waittime.status_code == 200:
            data["waittime"] = response_waittime.json()
    except Exception as e:
        print(f"  Error fetching wait time data: {e}")
    
    return data


def save_jfk_to_csv(data, filename="jfk_walk_times.csv"):
    """Save JFK walk times data to CSV."""
    if "walktime" not in data or "terminals" not in data["walktime"]:
        print(f"  No valid JFK walk time data to save")
        return
    
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["airport", "terminal_name", "gate_name", "walk_time"])
            
            for terminal in data["walktime"]["terminals"]:
                terminal_name = terminal["terminalName"]
                for gate in terminal["gateNames"]:
                    writer.writerow([
                        "JFK",
                        terminal_name,
                        gate["gateName"],
                        gate["walkTime"],
                    ])
        
        print(f"  ✓ Saved JFK data to {filename}")
    except Exception as e:
        print(f"  Error saving JFK data: {e}")


def save_combined_to_csv(heathrow_data, jfk_data, filename="raw_airport_data.csv"):
    """Save combined airport data to CSV."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "airport", "data_type", "details"])
            
            # Heathrow data
            writer.writerow([
                heathrow_data["timestamp"],
                "Heathrow",
                "Security Wait Time",
                str(heathrow_data.get("security", "N/A")),
            ])
            
            if "immigration" in heathrow_data:
                for terminal, data in heathrow_data["immigration"].items():
                    writer.writerow([
                        heathrow_data["timestamp"],
                        "Heathrow",
                        f"Immigration ({terminal})",
                        str(data),
                    ])
            
            # JFK data
            writer.writerow([
                jfk_data["timestamp"],
                "JFK",
                "Walk Times",
                str(jfk_data.get("walktime", "N/A")),
            ])
            writer.writerow([
                jfk_data["timestamp"],
                "JFK",
                "Wait Times",
                str(jfk_data.get("waittime", "N/A")),
            ])
        
        print(f"  ✓ Saved combined data to {filename}")
    except Exception as e:
        print(f"  Error saving combined data: {e}")


if __name__ == "__main__":
    
    heathrow_data = fetch_heathrow_data()
    jfk_data = fetch_jfk_data()
    
    print("\nSaving data to CSV...")
    save_jfk_to_csv(jfk_data)
    save_combined_to_csv(heathrow_data, jfk_data)
    
