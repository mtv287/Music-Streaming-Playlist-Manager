import random

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line = file.readline()
        return eval(line.strip()) if line.strip() else []
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Creating a new one...")
        return []

def write_file(file_path, playlist_cdll):
    try:
        song_list = []
        if not playlist_cdll.isEmpty():
            current = playlist_cdll.head
            while True:
                song_list.append((
                    current.data.song_id, current.data.title, 
                    current.data.artist, current.data.duration, current.data.genre
                ))
                current = current.next
                if current == playlist_cdll.head:
                    break
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(song_list))
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# CORE CLASSES
class Song:
    def __init__(self, song_id=None, title=None, artist=None, duration=None, genre=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration = duration
        self.genre = genre

    def __str__(self):
        return f"({self.song_id}, {self.title}, {self.artist}, {self.duration}s, {self.genre})"

# ĐỔI SANG DOUBLY NODE (Thêm con trỏ prev)
class songNode: 
    def __init__(self, _data, _next=None, _prev=None):
        self.data = _data
        self.next = _next
        self.prev = _prev  # Con trỏ trỏ tới bài phía trước

# CIRCULAR DOUBLY LINKED LIST (CDLL)
class CircularDoublyLinkedList: 
    def __init__(self):
        self.head = None
        self.current_track = None

    def isEmpty(self):
        return self.head is None

    def addSong(self, new_data):
        new_node = songNode(new_data)
        if self.isEmpty():
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current_track = new_node
        else:
            tail = self.head.prev  # Nút cuối luôn là head.prev trong CDLL
            
            # Cập nhật liên kết cho nút mới
            new_node.next = self.head
            new_node.prev = tail
            
            # Cập nhật liên kết nút head và tail cũ
            tail.next = new_node
            self.head.prev = new_node

    def removeSong(self, song_id):
        if self.isEmpty():
            print("Empty!!")
            return None

        current = self.head
        found_node = None

        # Tìm nút cần xóa
        while True:
            if current.data.song_id == song_id:
                found_node = current
                break
            current = current.next
            if current == self.head:
                break

        if not found_node:
            print("no song match")
            return None

        # Nếu danh sách chỉ có 1 nút
        if found_node.next == found_node:
            self.head = None
            self.current_track = None
            return found_node.data

        # Điều chỉnh con trỏ phát nhạc nếu bài bị xóa đang phát
        if self.current_track == found_node:
            self.current_track = found_node.next

        # Xóa nút bằng cách nối prev và next của các nút xung quanh (O(1))
        found_node.prev.next = found_node.next
        found_node.next.prev = found_node.prev

        # Nếu nút bị xóa là head
        if found_node == self.head:
            self.head = found_node.next

        return found_node.data

    def nextSong(self):
        """Chuyển sang bài tiếp theo (Tiến - O(1))"""
        if self.isEmpty() or self.current_track is None:
            return None
        old_song = self.current_track.data
        self.current_track = self.current_track.next
        return old_song

    def prevSong(self):
        """Quay lại bài phía trước (Lùi - O(1) nhờ CDLL)"""
        if self.isEmpty() or self.current_track is None:
            return None
        self.current_track = self.current_track.prev
        return self.current_track.data

    def displayAll(self):
        if self.isEmpty():
            print("Empty playlist")
            return None
        current = self.head
        while True:
            marker = " -> [Playing]" if current == self.current_track else ""
            print(f"{current.data}{marker}")
            current = current.next
            if current == self.head:
                break
        print("=========")

# STACK DATA STRUCTURE (Dùng làm Lịch sử nghe nhạc)
class StackNode:
    def __init__(self, info):
        self.info = info
        self.next = None

class RecentlyPlayedStack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self, song):
        new_node = StackNode(song)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.is_empty():
            return None
        tmp = self.top
        self.top = self.top.next
        return tmp.info

    def display_history(self):
        print("Recently Played History (Stack - LIFO):")
        if self.is_empty():
            print("No history")
        else:
            current = self.top
            while current:
                print(f"   [Past] {current.info}")
                current = current.next
        print("=========")

# CONTROLLER
class MusicPlayer:
    def __init__(self, file_path="playlist.txt"):
        self.file_path = file_path
        self.playlist = CircularDoublyLinkedList()  # Cập nhật sang CDLL
        self.history = RecentlyPlayedStack()
        self.song_hash_map = {}

    def load_data_from_file(self):
        raw_data = read_file(self.file_path)
        for song_info in raw_data:
            song_obj = Song(song_info[0], song_info[1], song_info[2], song_info[3], song_info[4])
            self.playlist.addSong(song_obj)
            self.song_hash_map[song_obj.song_id] = song_obj

    def play_current(self):
        if self.playlist.isEmpty() or self.playlist.current_track is None:
            print("No song in playlist.")
            return
        print(f"🎵 Now Playing: {self.playlist.current_track.data}")

    def skip_next(self):
        """Phát bài tiếp theo"""
        if self.playlist.isEmpty():
            return
        old_song = self.playlist.nextSong()
        if old_song:
            self.history.push(old_song)
        print(f"⏭️ Skipped Next!")
        self.play_current()

    def go_previous(self):
        """Tận dụng trực tiếp prevSong() của CDLL với độ phức tạp O(1)"""
        if self.playlist.isEmpty():
            return
        prev_song = self.playlist.prevSong()
        print(f"⏮️ Went Back to Previous Song (CDLL Prev)!")
        print(f"🎵 Now Playing: {prev_song}")

    def shuffle_play(self):
        if self.playlist.isEmpty():
            return
        all_nodes = []
        curr = self.playlist.head
        while True:
            all_nodes.append(curr)
            curr = curr.next
            if curr == self.playlist.head:
                break
            
        random_node = random.choice(all_nodes)
        if self.playlist.current_track:
            self.history.push(self.playlist.current_track.data)
        self.playlist.current_track = random_node
        print(f"🔀 Shuffle Triggered!")
        self.play_current()
    
    def add_new_song(self, song):
        self.playlist.addSong(song)
        self.song_hash_map[song.song_id] = song
        write_file(self.file_path, self.playlist)

    def remove_song_by_id(self, song_id):
        removed = self.playlist.removeSong(song_id)
        if removed:
            if song_id in self.song_hash_map:
                del self.song_hash_map[song_id]
            write_file(self.file_path, self.playlist)
            print(f"--- Successfully removed: {removed} ---")

# MENU CHẠY THỬ
def main():
    player = MusicPlayer("playlist.txt")
    player.load_data_from_file()

    while True:
        print("\n=== MUSIC STREAMING PLAYLIST MANAGER (CDLL) ===")
        player.playlist.displayAll()
        player.history.display_history()
        player.play_current()
        
        print("\nSelect an action:")
        print("1. Next Song (Skip Next)")
        print("2. Previous Song (Go Back via CDLL)")
        print("3. Shuffle Play")
        print("4. Add Song")
        print("5. Remove Song by ID")
        print("0. Exit")
        
        choice = input("Enter choice (0-5): ")
        print("\nOUTPUT:")
        if choice == "1":
            player.skip_next()
        elif choice == "2":
            player.go_previous()
        elif choice == "3":
            player.shuffle_play()
        elif choice == "4":
            s_id = input("  ID: ")
            s_title = input("  Title: ")
            s_artist = input("  Artist: ")
            s_duration = int(input("  Duration: "))
            s_genre = input("  Genre: ")
            player.add_new_song(Song(s_id, s_title, s_artist, s_duration, s_genre))
        elif choice == "5":
            r_id = input("Enter Song ID to remove: ")
            player.remove_song_by_id(r_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()