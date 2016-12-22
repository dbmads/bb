
class Config(object):
    ADMIN_EMAIL = "your_email@gmail.com"

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = 'write-a-secret-string-here'
    LISTINGS_PER_PAGE = 5

    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'add_salt_123_hard_one'
    SECURITY_CONFIRMABLE = True

