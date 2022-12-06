from flask import Flask
from app.config import Config
from app import db

app = Flask(__name__)
app.config.from_object("app.config.Config")
db.create_database_connection(Config.DATABASE_URL)
db.create_session()

from app import routes  # noqa: #F401, E402

db.create_tables()
