import sqlite3

import sqlite3
import os

# This gets the exact folder where THIS setup file is saved
folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder, 'social_media.db')


connention = sqlite3.connect(db_path)

cursor = connention.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
        user_id INTEGER,
        video_id INTEGER,
        watch_time INTEGER,
        total_duration INTEGER,
        audio_id TEXT,
        is_liked INTEGER,
        is_shared INTEGER,
        is_saved INTEGER)
''')

connention.commit()
connention.close()