#!/usr/bin/env python
import os
import nose

os.environ['ENVIRONMENT'] = "testing"
os.environ['FLASK_ENV'] = "testing"
nose.main()
