#!/usr/bin/python3

# this is for Apache - doe not matter in dev



import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/cube/current")

from cube import create_app
application = create_app()
