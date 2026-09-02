# Authentic 100% Real Football Player Database Builder
import os
import sys
import sqlite3
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_db_connection, init_db
from pipeline.generate_expanded_data import get_mega_player_dataset
from pipeline.build_db import score_to_grade

print('Imports OK')
