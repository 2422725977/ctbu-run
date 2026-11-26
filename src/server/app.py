from flask import Flask, jsonify, request, session

app = Flask(__name__)


def _body():
    return request.get_json(silent=True) or {}


def _ok(**kw):
    return jsonify(dict(ok=True, **kw))


@app.get("/console")
def console():
    rows = session.get("accounts") or []
    return _ok(accounts=[{"id": a.get("id"), "quota": a.get("quota", 0)} for a in rows])


@app.get("/api/account/token")
def account_token():
    row = (session.get("accounts") or [{}])[0]
    return _ok(token=row.get("token", ""))


@app.post("/api/account/schedule")
def account_schedule():
    b = _body()
    scope = (session.setdefault("schedule", {})).setdefault(b.get("id", ""), {})
    scope.update({k: b[k] for k in ("days", "start", "end") if k in b})
    return _ok(schedule=scope)
