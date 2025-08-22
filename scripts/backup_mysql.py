import datetime, subprocess, pathlib

DB="nyc_taxi"
OUT=pathlib.Path("./backups"); OUT.mkdir(exist_ok=True)
stamp=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
dump=OUT/f"{DB}-{stamp}.sql"

cmd=["mysqldump","-h","127.0.0.1","-uroot","-ppass","--single-transaction",DB]
print("[backup] running:", " ".join(cmd[:-1] + ["***", DB]))
with open(dump,"wb") as f:
    r=subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)
print("[backup] OK:", dump, "size:", dump.stat().st_size)

# Light integrity probe
txt = dump.read_text(errors="ignore")
if "CREATE TABLE `yellow_trips`" not in txt:
    raise SystemExit("[backup] WARNING: expected schema not found.")
print("[backup] integrity probe passed.")
