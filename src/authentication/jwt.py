import jwt

from src.dto.schemas import User


class JwtEncoder:
    def encode(self, user: User):
        return jwt.encode(user.__dict__, "secret", algorithm='HS256')

    def decode(self, token: str):
        return User(**jwt.decode(token, "secret", algorithms=['HS256']))