import bcrypt

class PasswordEncoder:
    def encode(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def is_valid(self, hashed_password: str, entered_password: str) -> bool:
        return bcrypt.checkpw(entered_password.encode(), hashed_password.encode())