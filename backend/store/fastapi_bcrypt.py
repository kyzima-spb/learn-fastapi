from __future__ import annotations
import typing as t

import bcrypt


class Bcrypt:
    def _to_bytes(self, s: t.Union[str, bytes]) -> bytes:
        if isinstance(s, str):
            s = s.encode('utf-8')
        return s

    def generate_password_hash(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(self._to_bytes(password), salt)

    def check_password_hash(self, hashed_password: t.Union[str, bytes], password: str) -> bool:
        return bcrypt.checkpw(
            self._to_bytes(password),
            self._to_bytes(hashed_password),
        )
