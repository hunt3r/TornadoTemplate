
import tornado
import logging, logging.config
import tornado.template
from tornado.log import LogFormatter as TornadoLogFormatter
from tornado.options import define, options
import os
import motor

# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

# Deployment Configuration
class DeploymentType:
    PRODUCTION = "PROD"
    DEV = "DEV"
    SOLO = "LOCAL"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

APP_NAME="ExampleApp"
ENV_VAR="app_environment"
DEPLOYMENT = os.environ.get(ENV_VAR, DeploymentType.SOLO).upper()


STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

define("port", default=8000, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")

settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = STATIC_ROOT
settings['cookie_secret'] = "a816ebb3ca1e860eee5bd5cc8fbe56b1e440398e"
settings['auth_header'] = "X-%s-Auth" % APP_NAME
settings['xsrf_cookies'] = False
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)

###########################################################################
# General DB Settings
###########################################################################
settings['mongo'] = {}
settings['mongo']['host'] = "localhost"
settings['mongo']['port'] = 27017
settings['mongo']['db'] = APP_NAME
settings['db'] = motor.MotorClient("mongodb://%s:%s" % (settings['mongo']['host'], settings['mongo']['port']))[settings['mongo']['db']]

LOG_LEVEL="INFO"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(processName)-10s: %(name)-15s %(levelname)-8s %(message)s",
        },
        'tornado': {
                '()': TornadoLogFormatter,
                'fmt': '%(color)s[%(levelname)1.1s %(asctime)s %(name)s.%(funcName)s:%(lineno)d]%(end_color)s %(message)s',
                'color': True
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "tornado",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "transmit": {
            "level": LOG_LEVEL,
            "propagate": False,
            "handlers": ["console"]
        },
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

if options.config:
    tornado.options.parse_config_file(options.config)
