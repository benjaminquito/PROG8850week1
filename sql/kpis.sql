-- Daily KPIs
SELECT DATE(tpep_pickup_datetime) AS d,
       COUNT(*) AS trips,
       ROUND(SUM(total_amount),2) AS revenue,
       ROUND(SUM(tip_amount),2) AS tips
FROM yellow_trips
GROUP BY d
ORDER BY d;

-- Top 10 pickup zones
SELECT z.Zone, COUNT(*) AS trips
FROM yellow_trips t
JOIN taxi_zone_lookup z ON z.LocationID = t.PULocationID
GROUP BY z.Zone
ORDER BY trips DESC
LIMIT 10;
