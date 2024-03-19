from dataclasses import dataclass


@dataclass
class Token:
    grant: str| None 
    refresh_token: str