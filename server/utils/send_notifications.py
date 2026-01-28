# Copyright (c) 2024 PLANKA Software GmbH
# Licensed under the Fair Use License: https://github.com/plankanban/planka/blob/master/LICENSE.md

import sys
import json
from apprise import Apprise, LogCapture, logging

type Services = list[dict[str, str]]


def notify(services: Services, title: str, body: str, format: str) -> None:
    """Emit a notification and write warnings to stderr"""
    app = Apprise(servers=[s["url"] for s in services])
    with LogCapture(level=logging.WARNING) as warnings:
        app.notify(title=title, body=body, body_format=format)
        if warn := warnings.getvalue():  # type: ignore
            print(warn, file=sys.stderr)  # type: ignore
            sys.exit(1)


def notify_all(*args: str) -> None:
    srvs: Services = json.loads(args[1])
    title: str = args[2]
    bodies: dict[str, str] = json.loads(args[3])
    # Get unique formats and bundle service notifiers by format and notify
    for fmt in set(s["format"] for s in srvs):
        notify(
            services=[s for s in srvs if s["format"] == fmt],
            title=title,
            body=bodies[fmt],
            format=fmt,
        )


if __name__ == "__main__":
    notify_all(*sys.argv)
