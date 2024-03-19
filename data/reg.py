from dataclasses import dataclass

@dataclass
class RegisterForm:
    username: str
    email: str
    password: str


