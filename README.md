# Harverster
This code is meant to run on a `Raspberry Pi` served by `Ubuntu 22` through `Docker`.
This code have to collect metrics from hardware and send it to the Nester though an SHH tunnel to access the NoSQL DataBase.

# Capabilities:
- Get params from the env (like the name of the harvester, frequency of collection, endpoint of the Nester, etc)
- Collect metrics from the hardware
- execute scan from Nmap (Issue with docker ? bridge connection ?)
- Send metrics to the Nester through an SHH tunnel
- Be able to receive commande from the Nester through the SHH tunnel
- Be able to send a health check to the Nester through the SHH tunnel

## Technical layer:
- Python3.12
- MongoDB (for Nester)
- OOP

### Database schema:
```
{
  "collectorName": "unique_collector_name",
  "timeOfCollect": "actual time",
  "metrics": {
    "cpu": {
      "usage": "45%",
      "cores": 4,
      "temperature": "55C"
    },
    "memory": {
      "total": "16GB",
      "used": "8GB",
      "free": "8GB"
    },
    "disk": [
      {
        "diskName": "Disk 1",
        "capacity": "1TB",
        "used": "500GB",
        "free": "500GB"
      },
      {
        "diskName": "Disk 2",
        "capacity": "500GB",
        "used": "200GB",
        "free": "300GB"
      }
    ]
  },
  "nmapScanOutput": "raw_nmap_output_here"
}```
