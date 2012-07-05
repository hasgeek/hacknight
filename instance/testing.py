"""
Test configuration for Hacknight
"""

#: Timezone for displayed datetimes
TIMEZONE = 'Asia/Calcutta'
#: Database backend
SQLALCHEMY_DATABASE_URI = 'sqlite:///'
#: Secret key
SECRET_KEY = 'test' 
#: Folderto upload the participants list
UPLOAD_FOLDER = 'uploads/'
#: Supported extensions
ALLOWED_EXTENSIONS = set(['txt', 'csv'])
#: LastUser server
LASTUSER_SERVER = 'test'
#: LastUser client id
LASTUSER_CLIENT_ID = 'test'
#: LastUser client secret
LASTUSER_CLIENT_SECRET = 'test'
#: Mail settings
#: MAIL_FAIL_SILENTLY : default True
MAIL_SERVER = 'test'
#: MAIL_PORT : default 25
#: MAIL_USE_TLS : default False
#: MAIL_USE_SSL : default False
MAIL_USERNAME = 'test'
MAIL_PASSWORD = 'test'
