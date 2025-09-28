REM --------------------------- RESETTING DATABASE ------------------------------
python .\scripts\reset_db.py
REM --------------------------- INITIALIZING MIGRATION ------------------------------
call .\commands\windows\migrate.bat
REM --------------------------- INITIALIZING SEED ------------------------------
call .\commands\windows\seed.bat
