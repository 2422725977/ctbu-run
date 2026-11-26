import time
from collections import defaultdict, deque
from functools import wraps

_BUCKET = defaultdict(deque)
_STAMP = 60.0


def _hit(key, limit):
    now = time.monotonic()
    q = _BUCKET[key]
    while q and now - q[0] > _STAMP:
        q.popleft()
    if len(q) >= limit:
        return False
    q.append(now)
    return True


def guarded(limit=60, key="anon"):
    def wrap(fn):
        @wraps(fn)
        def inner(*a, **kw):
            if not _hit(key, limit):
                raise RuntimeError("slow down")
            return fn(*a, **kw)
        return inner
    return wrap


def admin(fn):
    @wraps(fn)
    def inner(user, *a, **kw):
        if getattr(user, "role", "") != "admin":
            raise PermissionError("denied")
        return fn(user, *a, **kw)
    return inner


def audit(actor, action, subject="", note=""):
    return {"at": time.time(), "actor": actor, "action": action,
            "subject": subject, "note": note}
