# -*- coding: utf-8 -*-
#: Site title
SITE_TITLE = 'HasGeek Hacknight'
#: Site id (for network bar)
SITE_ID = 'hacknight'
#: Timezone
TIMEZONE = 'Asia/Calcutta'
#secret key
SECRET_KEY = '5\x07\xcf\xdb\xb2\x1b\xbb\x8a\x984W\xd1\x0faN\xd3U\xabb\xf2[\xb2\xd2\xf1\x13\x1c\xe7W&\t\xd9\xdb'
#: Database backend
SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
#: LastUser server
#LASTUSER_SERVER = 'https://auth.hasgeek.com/'
#LASTUSER_SERVER = 'https://login.hasgeek.com/'
LASTUSER_SERVER = 'http://lastuser.local:7000/'
#: LastUser client id
LASTUSER_CLIENT_ID = 'SL1E163NT5yCDVt9K8OoxQ'
#: LastUser client secret
LASTUSER_CLIENT_SECRET = 'Kj4SkuNjRj68xaFn2b6zIgtEpIcpwVRkGFlEl6SZQNCA'
#: Typekit id
TYPEKIT_CODE = 'qhx6vtv'
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
DEFAULT_MAIL_SENDER = ('HasGeek', 'bot@hasgeek.com')
#: Logging: recipients of error emails
ADMINS = ['kiran@hasgeek.com']
#: Log file
LOGFILE = 'error.log'
