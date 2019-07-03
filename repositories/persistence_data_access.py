from settings import Settings
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine(Settings.CONNECTION_STRING, use_batch_mode=True)
Session = sessionmaker(bind=engine)
session = Session()
