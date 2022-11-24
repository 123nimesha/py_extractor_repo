import os
import sys
from pathlib import Path
sys.path.append(os.path.join(os.path.split(__file__)[0], Path(__file__).resolve().parents[1], 'lib'))
sys.path.append(os.path.join(os.path.split(__file__)[0], Path(__file__).resolve().parents[1], 'util'))
import slack
import config
import db_config
import comm_lib