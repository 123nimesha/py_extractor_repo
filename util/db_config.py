import mysql.connector
import json
from pathlib import Path
import os
f = open(os.path.join(os.path.split(__file__)[0], Path(
    __file__).resolve().parents[1], 'config', 'config.json'), encoding='utf-8')
config_file = json.load(f)
env = config_file['env']


def db_connection():
    db = mysql.connector.connect(
        host=config_file['development_database']['host'] if env == 'development' else config_file['production_database']['host'],
        user=config_file['development_database']['user'] if env == 'development' else config_file['production_database']['user'],
        password=config_file['development_database']['password'] if env == 'development' else config_file['production_database']['password'],
        database=config_file['development_database']['database'] if env == 'development' else config_file['production_database']['database']
    )
    cursor = db.cursor()

    return {'db': db, 'cursor': cursor}
