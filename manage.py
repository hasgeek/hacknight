#! /usr/bin/env python

from coaster.manage import init_manager

from hacknight import app, init_for
from hacknight.models import db


if __name__ == "__main__":
    manager = init_manager(app, db, init_for)
    manager.run()
