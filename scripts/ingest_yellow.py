import os, io, csv, sys, pathlib, requests
from datetime import datetime
from dotenv import load_dotenv
import pyarrow.parquet as pq
import pymysql

load_dotenv()
HOST=os.getenv("MYSQL_HOST","127.0.0.1")
USER=os.getenv("MYSQL_USER","root")
PWD=os.getenv("MYSQL_PASSWORD","pass")
DB=os.getenv("MYSQL_DB","nyc_taxi")
DATA_DIR=pathlib.Path(os.getenv("DATA_DIR","./data")); DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "logs").mkdir(exist_ok=True)

BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{ym}.parquet"

COLUMNS = [
 "VendorID","tpep_pickup_datetime","tpep_dropoff_datetime","passenger_count",
 "trip_distance","RatecodeID","store_and_fwd_flag","PULocationID","DOLocationID",
 "payment_type","fare_amount","extra","mta_tax","tip_amount","tolls_amount",
 "improvement_surcharge","total_amount","congestion_surcharge","airport_fee","cbd_congestion_fee"
]

def download_parquet(ym: str) -> pathlib.Path:
    url = BASE.format(ym=ym)
    out = DATA_DIR / f"yellow_{ym}.parquet"
    print(f"[download] {url}")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(out, "wb") as f:
            for chunk in r.iter_content(1<<20):
                f.write(chunk)
    return out

def load_month(ym: str):
    pqt = download_parquet(ym)

    # Stream row groups to CSV for LOAD DATA
    pf = pq.ParquetFile(pqt)
    tmp_csv = DATA_DIR / f"yellow_{ym}.csv"
    with open(tmp_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS + ["_ingest_month"])
        for i in range(pf.num_row_groups):
            batch = pf.read_row_group(i, columns=COLUMNS).to_pandas()

            # Basic cleaning
            batch = batch[(batch["trip_distance"] >= 0) & (batch["fare_amount"] >= -5)]
            batch["_ingest_month"] = ym
            batch = batch.fillna("")
            w.writerows(batch.values.tolist())

    # Bulk load
    conn = pymysql.connect(host=HOST, user=USER, password=PWD, database=DB,
                           local_infile=True, autocommit=True, charset="utf8mb4")
    with conn.cursor() as cur:
        cur.execute("SET SESSION sql_log_bin=0;")
        load_sql = f"""
        LOAD DATA LOCAL INFILE %s
        INTO TABLE yellow_trips
        FIELDS TERMINATED BY ',' ENCLOSED BY '"'
        LINES TERMINATED BY '\\n'
        IGNORE 1 LINES
        ({",".join(COLUMNS)}, _ingest_month)
        """
        cur.execute(load_sql, (str(tmp_csv),))
    conn.close()
    print(f"[ingest] Loaded {ym}")

if __name__ == "__main__":
    months = sys.argv[1:] or ["2024-01","2024-02","2024-03"]
    for ym in months:
        load_month(ym)
    print("[done] Ingestion complete.")
