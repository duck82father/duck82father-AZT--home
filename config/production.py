from logging.config import dictConfig
from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'homepage.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'Q\xa1|\x8c^\xbf\x84i\xca\x081 \xf4\xd5\xf7\xbf'

dictConfig({
    'version' : 1,
    'formatters' : {
        'default' : {
            'format' : '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
    },
    'handlers': {
        'file' :{
            'level' : 'INFO',
            'class' : 'logging.handlers.RotatingFileHandler',
            'filename' : os.path.join(BASE_DIR, 'logs/myproject.log'),
            'maxBytes' : 1024 * 1024 * 5, # 5 MB
            'backupCount' : 5,
            'formatter' : 'default',
        },
    },
    'root' : {
        'level' : 'INFO',
        'handlers' : ['file']
    }
})