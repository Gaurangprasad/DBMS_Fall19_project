python3 -m pip install -r requirements.txt

createuser -U postgres itws_final
createdb -U postgres -O itws_final final_db
psql -U postgres -d final_db -f create_user.sql
psql -U postgres -f schema.sql

python load_data.py

