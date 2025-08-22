# NYC Taxi ETL + Automation — Starter Repo

This starter kit sets up a **repeatable pipeline** to ingest NYC TLC Yellow Taxi data into **MySQL**, compute daily KPIs, and run **automated backups**.

## What’s inside
- `docker-compose.yml` — MySQL 8 + Adminer (one-command start)
- `sql/schema.sql` — Tables (`yellow_trips`, `taxi_zone_lookup`) + indexes
- `sql/health.sql` — Simple health checks
- `sql/kpis.sql` — Daily KPIs and top zones
- `scripts/ingest_yellow.py` — Download (Parquet) → transform → bulk load
- `scripts/backup_mysql.py` — Nightly backup + quick integrity probe
- `config/.env.example` — Environment config (copy to `.env` and edit)
- `requirements.txt` — Python dependencies
- `cron_examples.txt` — Sample schedules (Linux/macOS + Windows)

## Quick start
1. **Install Docker** and **Python 3.10+**.
2. Start services:
   ```bash
   docker compose up -d
   ```
   MySQL: `localhost:3306` (`root`/`pass`), Adminer UI at http://localhost:8080
3. Create and seed schema:
   ```bash
   mysql -h127.0.0.1 -uroot -ppass < sql/schema.sql
   ```
4. Create a virtual env and install deps:
   ```bash
   python -m venv .venv && . .venv/bin/activate  # (Windows: .venv\Scripts\activate)
   pip install -r requirements.txt
   cp config/.env.example .env  # then edit values if needed
   ```
5. Ingest 3 months to test:
   ```bash
   python scripts/ingest_yellow.py 2024-01 2024-02 2024-03
   ```
6. Load taxi zone lookup:
   ```bash
   mysql -h127.0.0.1 -uroot -ppass nyc_taxi -e "SET GLOBAL local_infile=1;"
   mysql -h127.0.0.1 -uroot -ppass nyc_taxi -e \     "LOAD DATA LOCAL INFILE 'data/taxi_zone_lookup.csv' INTO TABLE taxi_zone_lookup \      FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES \      (LocationID, Borough, Zone, service_zone);"
   ```
7. Run KPIs:
   ```bash
   mysql -h127.0.0.1 -uroot -ppass nyc_taxi < sql/kpis.sql
   ```
8. Backup:
   ```bash
   python scripts/backup_mysql.py
   ```

## Notes
- **Passwords:** never commit `.env` to Git. Use `.env.example` as a template.
- **Reproducibility:** scripts are idempotent; re-running months will append with an `_ingest_month` tag.
- **Scale up:** Once stable, load additional months (entire 2024 or 2025 YTD).

## References
- NYC TLC Trip Data portal (monthly Parquet), Yellow Taxi Data Dictionary, and zone lookups.
