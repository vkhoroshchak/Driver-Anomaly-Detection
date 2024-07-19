# Driver-Anomaly-Detection

## Overview
This project is a simple driver anomaly detection system that processes geo data records and detects anomalies in the data. 
The system is built using Python and FastAPI, and uses Prometheus for metrics tracking.
In addition, it includes a script to generate random geo data records for testing purposes.

---
## Getting Started

### Prerequisites
Before diving into the setup process, ensure that Docker and Docker Compose are installed on your system.

### Setup Instructions
Follow these straightforward steps to get the application up and running:

1. **Clone the Repository**: Start by cloning this repository to your local machine.

2. **Navigate to the Project Directory**: Open a terminal window and move to the project directory.

3. **Start the Application**:
   
   Run the following command to initiate the application in detached mode:

   ```bash
   docker-compose up -d
   ```

   Alternatively, if you have a Makefile available, you can use:

   ```bash
   make start
   ```
---

## Metrics

This project uses Prometheus counters to track various metrics. Below are the metrics being recorded:

1. **Geo Data Records Received**
   - **Metric Name**: `received_geo_data_records_count`
   - **Description**: Counts the number of geo data records received.

2. **Driver Records with Overspeeding**
   - **Metric Name**: `driver_overspeeding_records_count`
   - **Description**: Counts the number of driver records with overspeeding incidents.

3. **Anomalous Altitude Coordinates Count**
   - **Metric Name**: `anomalous_altitude_coordinates_count`
   - **Description**: Counts the number of anomalous altitude coordinates detected.

4. **Database Writes Count**
   - **Metric Name**: `database_writes_count`
   - **Description**: Counts the number of writes to the database.

5. **Application Uptime in Seconds**
   - **Metric Name**: `app_uptime_seconds`
   - **Description**: Tracks the application uptime in seconds.

All metrics can be accessed at the `/metrics` endpoint.