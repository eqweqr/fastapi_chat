from alembic.config import Config
from alembic import command
from customlog import custom_logger

alembic_cfg = Config('/home/leo/python/last_one/alembic.ini')

def drop_last_migraiton():
    print(alembic_cfg)
    custom_logger.info('drop last migration')
    command.downgrade(alembic_cfg, '-1')

def upgrade_last_migration():
    print(alembic_cfg)
    custom_logger.info('upgrade last migration')
    command.upgrade(alembic_cfg, 'head')