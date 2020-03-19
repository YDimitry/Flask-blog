class Config:
    """ Common configuration """
    pass


class DevelopmentConfig(Config):
    """ Development configurations """
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    EXPLAIN_TEMPLATE_LOADING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #  в файле instance/config.py
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #
    # SECRET_KEY = ''
    # SQLALCHEMY_DATABASE_URI = r'sqlite:///' + os.path.join(BASE_DIR, 'blog.sqlite3')

class ProductionConfig(Config):
    """ Production configurations """
    ENV = 'production'
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
