import os

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
S3_BUCKET_NAME=os.environ.get('S3_BUCKET_NAME')
S3_SECRET_ACCESS_KEY=os.environ.get('S3_SECRET_ACCESS_KEY')
S3_ACCESS_KEY_ID=os.environ.get('S3_ACCESS_KEY_ID')
S3_LOCATION = 'https://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
