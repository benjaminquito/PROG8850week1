-- Row counts by day (last 7 days)
SELECT DATE(tpep_pickup_datetime) AS d, COUNT(*) AS trips
FROM yellow_trips
WHERE tpep_pickup_datetime >= NOW() - INTERVAL 7 DAY
GROUP BY d ORDER BY d;

-- Null/invalid checks
SELECT
  SUM(trip_distance < 0) AS bad_distance,
  SUM(total_amount IS NULL) AS null_total
FROM yellow_trips;
