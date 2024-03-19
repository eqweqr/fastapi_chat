from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel, validator

@dataclass
class Config():
    access_token_exp: int = 15
    refresh_token_exp: int = 90
    sql_db: str = 'psql://localhost:5432/test:password?auth'
    redis_db: str
    secret: str
    cry_alghorim: str
    

    def load_config(self, path: str):
        config = ConfigParser()
        with open(path) as fd:
            config.read_file(fd)
        self.access_token_exp = int(config.get('TOKEN', 'ACCESS_TOKEN_EXPIRE'))
        self.refresh_token_exp = config.get('TOKEN', 'REFRESH_TOKEN_EXPIRE')
        self.sql_db = config.get('TOKEN', 'SQL_DB')
        self.redis_db = config.get('TOKEN', 'REDIS_DB')
        self.secret = config.get('TOKEN', 'SECRET')
        self.cry_alghorim = config.get('TOKEN', 'ALGHORITHM')