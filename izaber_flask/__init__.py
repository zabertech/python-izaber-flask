import os
import importlib

import izaber
from izaber import config, app_config, autoloader
from izaber.startup import request_initialize, initializer
from izaber.log import log
from izaber.paths import paths

import flask

autoloader.add_prefix('izaber.flask')

CONFIG_BASE = """
default:
    debug: true
    flask:
        host: 127.0.0.1
        port: 5000

"""

class IZaberFlask(flask.Flask):

    allowed_protocol = None

    def __init__(self,*args,**kwargs):
        super(IZaberFlask,self).__init__(*args,**kwargs)
        self.allowed_protocol = None

    def app_protocol(self,path_info):
        return self.allowed_protocol

    def run(self, host=None, port=None, debug=None, **options):
        if host is None:
            host = config.flask.host
        if port is None:
            port = config.flask.port
        if debug is None:
            debug = config.debug
        super(IZaberFlask,self).run(
                                    host,
                                    port,
                                    debug,
                                    **options
                                )

app = IZaberFlask(__name__)

@initializer('flask')
def load_config(**kwargs):
    request_initialize('config',**kwargs)
    request_initialize('logging',**kwargs)
    config.config_amend_(CONFIG_BASE)

