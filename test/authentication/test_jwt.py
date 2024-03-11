from src.authentication.jwt import JwtEncoder
from src.dto.enums import UserRole
from src.dto.schemas import User


def test_jwt_encode_and_decode():
    user = User(id=1, email="lehadnk@gmail.com", role=UserRole.ADMIN)

    jwt_encoder = JwtEncoder()
    jwt = jwt_encoder.encode(user)

    assert jwt is not None
    assert len(jwt) > 40

    decoded_jwt = jwt_encoder.decode(jwt)
    assert decoded_jwt is not None
    assert isinstance(decoded_jwt, User)
    assert decoded_jwt.id == 1
    assert decoded_jwt.email == "lehadnk@gmail.com"
    assert decoded_jwt.role == UserRole.ADMIN