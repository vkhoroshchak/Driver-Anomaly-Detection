from prometheus_client import Counter

geo_data_records_received = Counter("received_geo_data_records_count", "Geo Data Records Received")
driver_records_with_overspeeding = Counter("driver_overspeeding_records_count", "Driver records with Overspeeding")
anomalous_altitude_coordinates_count = Counter(
    "anomalous_altitude_coordinates_count", "Anomalous Altitude Coordinates Count"
)
database_writes_count = Counter("database_writes_count", "Database Writes Count")
