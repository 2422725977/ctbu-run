import json
import os

TARGET = os.environ.get("PLATFORM_HOST", "example.invalid")
_MARK = "x-flow"


class Grab:
    def __init__(self, sink=None):
        self.sink = sink

    def request(self, flow):
        if TARGET not in getattr(flow.request, "pretty_host", ""):
            return
        flow.metadata[_MARK] = {"len": len(flow.request.content or b"")}

    def response(self, flow):
        st = (flow.metadata or {}).get(_MARK)
        if not st:
            return
        body = getattr(flow.response, "content", b"") or b""
        if self.sink:
            self.sink(json.dumps({"n": st["len"], "r": len(body)}))

    def finish(self):
        self.sink = None
