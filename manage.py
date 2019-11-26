#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cogofly.settings")
    # !! modification pour activer l'environnement https
    if os.path.realpath(os.path.curdir) == '/web/htdocs/cogofly/htdocs':
        os.environ.setdefault("HTTPS", "on")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
