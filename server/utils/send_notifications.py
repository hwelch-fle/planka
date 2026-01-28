# Copyright (c) 2024 PLANKA Software GmbH
# Licensed under the Fair Use License: https://github.com/plankanban/planka/blob/master/LICENSE.md

import sys
import json
from apprise import Apprise, LogCapture, logging

type Services = list[dict[str, str]]

class Notifier:
    def __init__(self, services: Services, title: str, body: str, format: str) -> None:
        self.app = Apprise(servers=[s["url"] for s in services])
        self.body = body
        self.fmt = format
        self.title = title

    def notify(self) -> None:
        """Emit a notification"""
        with LogCapture(level=logging.WARNING) as output:
            self.app.notify(title=self.title, body=self.body, body_format=self.fmt)
            if err := output.getvalue(): # type: ignore
                print(err, file=sys.stderr) # type: ignore


def notify(*args: str) -> None:
    srvs: Services = json.loads(args[1])
    title: str = args[2]
    bodies: dict[str, str] = json.loads(args[3])
    # Get unique formats and bundle service notifiers by format and notify
    for fmt in set(s["format"] for s in srvs)
        Notifier([s for s in srvs if s["format"] == fmt], title, bodies[fmt], fmt,).notify()

if __name__ == "__main__":
    notify(*sys.argv)
