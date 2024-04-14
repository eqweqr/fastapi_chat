from alembic.config import Config
from alembic import command
from customlog import custom_logger
import os
from pathlib import Path
import time

def get_alembic_config() -> Config:
    home = Path(os.getenv('HOME'))
    path_to_migration_file = home / 'work/fastapi_chat/fastapi_chat/alembic.ini'
    return Config(path_to_migration_file)

def run_downgrade(config: Config):
    custom_logger.info('Start downgrade migration')
    command.downgrade(config, '-1')


def run_upgrade(config: Config):
    custom_logger.info('Start upgrade migration')
    command.upgrade(config, 'head')

# cfg = get_alembic_config()
# run_upgrade(cfg)
# time.sleep(1)
# run_downgrade(cfg)