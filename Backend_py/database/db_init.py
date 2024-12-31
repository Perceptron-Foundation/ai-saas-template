import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from Backend_py.database import model
from Backend_py.database.db import engine

def init_db():
    try: 
        model.Base.metadata.create_all(bind=engine)
        logger.info("Database Initialized")
    except Exception as e:
        logger.error(f"Error while initializing database: {e}")
        raise e