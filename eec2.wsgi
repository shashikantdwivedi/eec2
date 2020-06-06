#!/home/ubuntu/miniconda3/envs/eec2/bin
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/eec2/eec2/")

from app import app as application
application.secret_key = 'SECRET-KEY' # TODO - Replace SECRET-KEY with your application secret key
