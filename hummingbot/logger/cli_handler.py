#!/usr/bin/env python

from datetime import datetime
from logging import StreamHandler
from typing import Optional

from hummingbot.client.config.i18n import gettext as _


class CLIHandler(StreamHandler):
    def formatException(self, _) -> Optional[str]:
        return None

    def format(self, record) -> str:
        exc_info = record.exc_info
        if record.exc_info is not None:
            record.exc_info = None
        retval = f'{datetime.fromtimestamp(record.created).strftime("%H:%M:%S")} - {record.name.split(".")[-1]} - ' \
                 f'{record.getMessage()}'
        if exc_info:
            retval += _(" (See log file for stack trace dump)")
        record.exc_info = exc_info
        return retval
