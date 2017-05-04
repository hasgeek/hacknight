#! /usr/bin/env python

from coaster.manage import init_manager

from hacknight import app
from hacknight.models import db


if __name__ == "__main__":
    manager = init_manager(app, db)
    manager.run()
