import os
import logging
from settings import constants


### Foundational Settings
cwd = os.path.dirname(__file__)
log_level = logging.DEBUG
cookie_secret = 'OMGSOOOOOSECRET'


### Directory Arrangement
dir_project = os.path.abspath(os.path.dirname(cwd))  ### cwd/../
dir_bin = os.path.join(dir_project, 'bin/')
dir_logs = os.path.join(dir_project, 'logs/')
dir_settings = os.path.join(dir_project, 'settings/')
dir_static = os.path.join(dir_project, 'static/')
dir_templates = os.path.join(dir_project, 'templates/')
