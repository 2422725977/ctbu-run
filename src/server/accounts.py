from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Account:
    student_num: str = ""
    alias: str = ""
    owner_id: int = 0
    quota: int = 0
    auth: dict = field(default_factory=dict)

    def __post_init__(self):
        self.student_num = str(self.student_num).strip()
        self.quota = max(0, int(self.quota or 0))
        self.auth = dict(self.auth or {})

    @property
    def usable(self):
        return bool(self.quota) and bool(self.auth.get("token"))

    def spend(self, n=1):
        if self.quota < n:
            return False
        self.quota -= n
        return True

    def as_row(self):
        out = asdict(self)
        out["auth"] = {"token": "***" if out["auth"].get("token") else ""}
        return out


def visible(rows, user_id, admin=False):
    return [r for r in rows if admin or r.owner_id == user_id]


def resolve(rows, key: Any):
    for r in rows:
        if str(r.student_num) == str(key):
            return r
    return None
