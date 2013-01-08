# -*- coding: utf-8 -*-
#: Site title
SITE_TITLE = 'HasGeek Hacknight'
#: Site id (for network bar)
SITE_ID = 'hacknight'
#: Database backend
SQLALCHEMY_DATABASE_URI = 'postgres://sqlalchemy:postgres-sqlalchemy@localhost:5432/hacknight'
#: Secret key
SECRET_KEY = 'make this something random'
#: Timezone
TIMEZONE = 'Asia/Calcutta'
#: LastUser server
LASTUSER_SERVER = 'https://auth.hasgeek.com/'
#: LastUser client id
LASTUSER_CLIENT_ID = 'AQvus4y5Trm5RZ71Fu-OCQ'
#: LastUser client secret
LASTUSER_CLIENT_SECRET = 'Rk4QqRuZSL25D-Bl3N5Wqw6AjlT6FdTQuSAiRgUIqNnA'
#: Mail settings
#: MAIL_FAIL_SILENTLY : default True
#: MAIL_SERVER : default 'localhost'
#: MAIL_PORT : default 25
#: MAIL_USE_TLS : default False
#: MAIL_USE_SSL : default False
#: MAIL_USERNAME : default None
#: MAIL_PASSWORD : default None
#: DEFAULT_MAIL_SENDER : default None
MAIL_FAIL_SILENTLY = False
MAIL_SERVER = 'localhost'
DEFAULT_MAIL_SENDER = ('HasGeek', 'test@example.com')
#: Logging: recipients of error emails
ADMINS = []
#: Log file
LOGFILE = 'error.log'
