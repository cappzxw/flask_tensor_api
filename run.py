import conf
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = "127.0.0.1:" + str(conf.SERVER_PORT)
accesslog = './log/gunicorn_access.log'
errorlog = './log/gunicorn_error.log'
