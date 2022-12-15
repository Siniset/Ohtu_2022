import logging
from flask import Flask
from app.config import Config
from app import db

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

app = Flask(__name__)
app.config.from_object("app.config.Config")
logging.info(f"Conncecting to database at {Config.DATABASE_URL}")
db.connect(app)

from app import routes  # noqa: #F401, E402

with app.app_context():
    db.connection.create_all()
    db.connection.session.commit()
