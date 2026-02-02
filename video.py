import sqlite3
import os
class VideoInteraction:
    def __init__(self, user_id,video_id, watch_time,total_duration, audio_id):
        self.user_id = user_id
        self.video_id = video_id
        self.watch_time = watch_time
        self.total_duration = total_duration
        self.audio_id = audio_id
        self.is_liked = False
        self.is_shared = False
        self.is_saved = False
    def __str__(self):
        return f"User {self.user_id} watched Video {self.video_id}"
    def calculate_completion(self):
        if self.total_duration == 0:
            return 0
        return (self.watch_time / self.total_duration) * 100
    def calculate_engagement_score(self):
        score = 0
        if self.is_liked:
            score += 1
        if self.is_saved:
            score += 3
        if self.is_shared:   
            score += 5    
        return score
class DataManager:
    def __init__(self, db_name='social_media.db'):
        self.interactions = []
        folder = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(folder, 'social_media.db')
    def fetch_data(self, raw_data):
        for entry in raw_data:
            interaction = VideoInteraction(
                user_id=entry['user_id'],
                video_id=entry['video_id'],
                watch_time=entry['watch_time'],
                total_duration=entry['total_duration'],
                audio_id=entry['audio_id']
            )
            interaction.is_liked = entry.get('is_liked', False)
            interaction.is_shared = entry.get('is_shared', False)
            interaction.is_saved = entry.get('is_saved', False)
            self.interactions.append(interaction)
    def save_to_db(self):
        """Saves all current interactions in memory to the SQLite database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for i in self.interactions:
            cursor.execute('''
                INSERT INTO interactions (user_id, video_id, watch_time, total_duration, audio_id, is_liked, is_shared, is_saved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                i.user_id, i.video_id, i.watch_time, i.total_duration, i.audio_id,
                int(i.is_liked), int(i.is_shared), int(i.is_saved)
            ))
        
        conn.commit()
        conn.close()
        print(f"Successfully saved {len(self.interactions)} interactions to database.")

    def load_from_db(self):
        """Clears current memory and loads all data from the database."""
        self.interactions = [] # Clear memory first
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, video_id, watch_time, total_duration, audio_id, is_liked, is_shared, is_saved FROM interactions')
        rows = cursor.fetchall()
        
        for row in rows:
            interaction = VideoInteraction(row[0], row[1], row[2], row[3], row[4])
            interaction.is_liked = bool(row[5])
            interaction.is_shared = bool(row[6])
            interaction.is_saved = bool(row[7])
            self.interactions.append(interaction)
            
        conn.close()
        print(f"Successfully loaded {len(self.interactions)} interactions from database.")


    def get_analytics(self):
        total_completion = 0
        high_engagement_videos = []
        audio_ids = {}
        for interaction in self.interactions:
            total_completion += interaction.calculate_completion()
            if interaction.calculate_engagement_score() >= 5:
                high_engagement_videos.append(interaction.video_id)
            if interaction.audio_id in audio_ids:
                audio_ids[interaction.audio_id] += 1
            else:
                audio_ids[interaction.audio_id] = 1
        avg_completion = total_completion / len(self.interactions) if self.interactions else 0
        most_used_audio = max(audio_ids, key=audio_ids.get) if audio_ids else None
        return {
            'average_completion': avg_completion,
            'high_engagement_videos': high_engagement_videos,
            'most_used_audio': most_used_audio
        }
    
    
if __name__ == "__main__":
    # 1. New data arriving from the 'frontend'
    raw_stream = [
        {'user_id': 1, 'video_id': 101, 'watch_time': 50, 'total_duration': 100, 'audio_id': 'A1', 'is_liked': True, 'is_saved': True},
        {'user_id': 2, 'video_id': 102, 'watch_time': 80, 'total_duration': 100, 'audio_id': 'A2', 'is_liked': True, 'is_shared': True},
        {'user_id': 3, 'video_id': 103, 'watch_time': 30, 'total_duration': 100, 'audio_id': 'A1'}
    ]

    manager = DataManager()

    # 2. Step: Ingest and Save
    manager.fetch_data(raw_stream)
    manager.save_to_db()

    # 3. Step: Prove the database works
    print("Clearing local memory...")
    manager.interactions = [] # Local list is now empty
    
    print("Loading data back from disk...")
    manager.load_from_db()

    # 4. Step: Final Report
    report = manager.get_analytics()
    if report:
        print("\n--- DATABASE-BACKED ANALYTICS REPORT ---")
        print(f"Avg Completion: {report['average_completion']:.2f}%")
        print(f"High Engagement IDs: {report['high_engagement_videos']}")
        print(f"Trending Audio: {report['most_used_audio']}")