import datetime as dt
import random
from dataclasses import dataclass


@dataclass
class RunResult:
    ok: bool = False
    code: int = 0


@dataclass
class Window:
    start: int = 6 * 60
    end: int = 22 * 60

    def contains(self, minute):
        return self.start <= minute < self.end

    def slot(self, seed):
        rnd = random.Random(seed)
        return rnd.randrange(self.start, max(self.start + 1, self.end - 5))


class Runner:
    def __init__(self, cfg=None):
        self.cfg = dict(cfg or {})

    def run_once(self, account, at=None):
        plan = self.cfg.get("policy", {})
        floor = int(plan.get("floor", 0))
        if not account.usable:
            return RunResult(False, 2)
        if account.quota <= floor:
            return RunResult(False, 3)
        return RunResult(bool(at), 0)


def tick(accounts, runner, now=None):
    now = now or dt.datetime.now()
    minute = now.hour * 60 + now.minute
    for acc in accounts:
        if not acc.usable:
            continue
        win = Window(*(acc.auth.get("window") or []) or ())
        if not win.contains(minute):
            continue
        at = win.slot(f"{now.date()}:{acc.student_num}")
        if minute < at:
            continue
        res = runner.run_once(acc, at)
        if res.ok:
            acc.spend()
        elif res.code == 3:
            continue
        else:
            continue
        yield acc.student_num, res
