T-2386 review (fm-reviewer, one pass): changes needed; fixed in 87a8ac8d before merge, red first (89 tests).
HIGH fixed: alembic's 'resolved database' check reread the ini fm wrote (circular), so an env.py taking its URL from app config reached the real dev database: a sitecustomize driver guard refuses every connect but the throwaway (sqlite3, sqlalchemy create_engine, psycopg2/psycopg/pymysql/MySQLdb), denials recorded and read back as refused; no unshare is named 'no network cut'.
MEDIUM fixed: psql -f as superuser ran repo SQL with meta-commands, COPY PROGRAM, dblink, fdw, pg_read_file, lo_*, CREATE EXTENSION: refused as unproven before a cluster starts.
MEDIUM fixed: script_location outside the copy skipped the check: refused. Django probe through manage.py shell -c. VACUUM INTO blocked.
MEDIUM fixed: every tool failure in a postgres-hinted tree read unproven: only dialect error text does; PG_ONLY extended and a sqlite syntax error retries on Postgres.
LOW fixed: Debian postgres paths, >1 MB files unproven, shlex-quoted short socket dir, migrations in version order, DB_VAR kept as defence in depth.
Open (builder's ponytail notes): the guard names listed drivers only (a C-level or unlisted driver or a direct sqlite3.Connection passes); a tool can delete the denial file; real alembic/Django/Postgres never ran here (stubs).
