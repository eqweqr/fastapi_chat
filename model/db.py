from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://test:password@localhost/start_alembic')
Session = sessionmaker(engine)