CREATE DATABASE IF NOT EXISTS nyc_taxi;
USE nyc_taxi;

CREATE TABLE IF NOT EXISTS taxi_zone_lookup (
  LocationID INT PRIMARY KEY,
  Borough VARCHAR(32),
  Zone VARCHAR(128),
  service_zone VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS yellow_trips (
  VendorID TINYINT,
  tpep_pickup_datetime DATETIME,
  tpep_dropoff_datetime DATETIME,
  passenger_count TINYINT,
  trip_distance DECIMAL(7,3),
  RatecodeID TINYINT,
  store_and_fwd_flag CHAR(1),
  PULocationID INT,
  DOLocationID INT,
  payment_type TINYINT,
  fare_amount DECIMAL(8,2),
  extra DECIMAL(8,2),
  mta_tax DECIMAL(8,2),
  tip_amount DECIMAL(8,2),
  tolls_amount DECIMAL(8,2),
  improvement_surcharge DECIMAL(8,2),
  total_amount DECIMAL(8,2),
  congestion_surcharge DECIMAL(8,2),
  airport_fee DECIMAL(8,2),
  cbd_congestion_fee DECIMAL(8,2),
  _ingest_month CHAR(7),
  KEY idx_pickup (tpep_pickup_datetime),
  KEY idx_pu_do (PULocationID, DOLocationID),
  KEY idx_payment (payment_type),
  KEY idx_month (_ingest_month)
);
