from src.authentication.authentication import PasswordEncoder


def test_password_hashing():
    raw_password = "qwe"

    password_encoder = PasswordEncoder()
    hashed_password = password_encoder.encode(raw_password)

    assert password_encoder.is_valid(hashed_password, raw_password)
    assert not password_encoder.is_valid(hashed_password, "123")