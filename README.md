# Harvester

This code is meant to run on a `Raspberry Pi` served by `Ubuntu 22` through `Docker`.
This code have to collect metrics from hardware and send it to the Nester though an SHH tunnel to access the NoSQL
DataBase.

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
  "nmapScanInput": "raw_nmap_input",
  "nmapScanOutput": "raw_nmap_output_here"
}
```

### Project structure:

```
Harvester/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── metric_collector/
│   │   ├── __init__.py
│   │   └── collector.py
│   ├── nmap_scanner/
│   │   ├── __init__.py
│   │   └── scanner.py
│   ├── ssh_client/
│   │   ├── __init__.py
│   │   └── client.py
│   ├── db_client/
│   │   ├── __init__.py
│   │   └── client.py
│   └── health_check/
│       ├── __init__.py
│       └── check.py
│
├── tests/
│   ├── __init__.py
│   ├── test_metric_collector.py
│   ├── test_nmap_scanner.py
│   ├── test_ssh_client.py
│   ├── test_db_client.py
│   └── test_health_check.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.sample
├── .gitignore
└── README.md
```

#### Breakdown:

- src/: This directory contains all the source code for the project.
    - main.py: The main application script that ties everything together.
    - metric_collector/: Module for collecting hardware metrics.
    - nmap_scanner/: Module for handling Nmap scans.
    - ssh_client/: Module for managing SSH communications.
    - db_client/: Module for interfacing with the MongoDB database.
    - health_check/: Module for performing health checks.
- tests/: Contains unit tests for each module.
    - test_metric_collector.py
    - test_nmap_scanner.py
    - test_ssh_client.py
    - test_db_client.py
    - test_health_check.py
- Dockerfile: Defines how to build the Docker container for the project.
- docker-compose.yml: Optionally used for managing the application with Docker Compose, especially if there are multiple
  services involved.
- requirements.txt: Lists all Python dependencies for the project.
- .env.sample: A sample environment file outlining the expected environment variables. This helps in setting up the
  project in different environments.
- .gitignore: Specifies files and directories that should be ignored by Git. Typically includes __pycache__/, .env, and
  other non-source files.
- README.md: A Markdown file containing information about the project, setup instructions, usage, and other
  documentation.
