# ## Phân rã bài toán — Music Streaming Playlist Manager

# **3 tính năng chính cần xây dựng:**
# - Phát lặp lại (repeat) → dùng **Circular Linked List**
# - Phát ngẫu nhiên (shuffle) → dùng **Random + CLL**
# - Quay lại bài trước (go back) → dùng **Stack**

# ---

# ## Phân chia công việc (5 người)

# **Người 1 — Node & Core Class**
# - Class `Song`: id, title, artist, duration, genre
# - Class `SongNode`: data (Song), next
# - Đây là nền cho cả nhóm, nên làm **trước nhất**

# **Người 2 — Circular Linked List**
# - Class `Playlist`: addSong(), removeSong(), displayAll()
# - Method `nextSong()` — logic vòng tròn để **phát lặp lại**
# - Giải thích tại sao CLL phù hợp cho repeat

# **Người 3 — Stack (Recently Played)**
# - Class `RecentlyPlayed`: push(), pop(), peek(), isEmpty()
# - push() gọi khi bắt đầu phát, pop() để **quay lại bài trước**
# - Giải thích LIFO phù hợp với tính năng go back

# **Người 4 — Shuffle & MusicPlayer**
# - Class `MusicPlayer` kết nối Playlist + RecentlyPlayed
# - Method `shufflePlay()` cho tính năng **phát ngẫu nhiên**
# - Method `playSong()`, `skipNext()`, `goBack()`

# **Người 5 — Report & Diagram**
# - Viết phần mô tả bài toán, lý do chọn cấu trúc dữ liệu
# - Vẽ sơ đồ quan hệ giữa các class (draw.io hoặc tay)
# - Tổng hợp, format, kiểm tra lại toàn bộ



import random

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line = file.readline()
        return eval(line.strip())
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Creating a new one...")
        return []

def write_file(file_path, playlist_cll):
    try:
        song_list = []
        if not playlist_cll.isEmpty():
            current = playlist_cll.tail.next
            while True:
                song_list.append((
                    current.data.song_id, current.data.title, 
                    current.data.artist, current.data.duration, current.data.genre
                ))
                if current == playlist_cll.tail:
                    break
                current = current.next
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(song_list))
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

#CORE CLASSES (Song & SongNode)
    
class Song:
    def __init__(self, song_id=None, title=None, artist=None, duration=None, genre=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration = duration
        self.genre = genre

    def __str__(self):
        return f"({self.song_id}, {self.title}, {self.artist}, {self.duration}s, {self.genre})"

class songNode: 
    def __init__(self,_data,_next):
        self.data=_data
        self.next=_next
    def displaySong(self):
        print(self.data)

#CIRCULAR LINKED LIST (Playlist)

class playList: 
    def __init__(self):
        self.tail=None
        self.current_track = None # Thêm biến này để biết đang phát đến bài nào độc lập

    def isEmpty(self):
        return self.tail==None

    def addSong(self,new_data):
        new_node=songNode(new_data,None)
        if self.isEmpty():
            self.tail=new_node
            new_node.next=new_node
            self.current_track = new_node #Khởi tạo bài phát đầu tiên
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node

    def removeSong(self, song_id):
        """Sửa nhẹ điều kiện so sánh từ đối tượng song sang song_id cho thực tế"""
        if self.isEmpty():
            print("Empty!!")
            return None
        
        # Đồng bộ con trỏ phát nhạc nếu bài sắp xóa trỏ đúng bài đang phát
        if self.current_track and self.current_track.data.song_id == song_id:
            self.current_track = self.current_track.next if self.tail != self.tail.next else None

        if self.tail == self.tail.next:
            if self.tail.data.song_id == song_id:
                valueSong = self.tail.data
                self.tail = None
                return valueSong
            else:
                print("no song match")
                return None
        else:
            current=self.tail.next
            prev=self.tail
            while True:
                if current.data.song_id == song_id:
                    valueSong=current.data
                    prev.next=current.next
                    if current == self.tail:
                        self.tail = prev
                    return valueSong
               
                prev=current   
                current=current.next
                if current == self.tail.next:
                    print("no song match")
                    return None

    def nextSong(self):
        #Hàm nhảy bài vòng tròn lặp vô tận (Repeat) 
        if self.isEmpty():
            return None
        else:
            # Lưu lại bài cũ trước khi nhảy
            old_song = self.current_track.data
            # Nhảy sang bài tiếp theo trong vòng tròn CLL
            self.current_track = self.current_track.next
            return old_song

    def displayAll(self):
        if self.isEmpty():
            print("Empty playlist")
            return None
        current=self.tail.next
        while True:
            marker = " -> [Playing]" if current == self.current_track else ""
            print(f"{current.data}{marker}")
            if current==self.tail:
                break
            current=current.next
        print("=========")

#STACK DATA STRUCTURE (Xây dựng lịch sử để làm tính năng "Go Back")

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

class QueueNode:
    def __init__(self, info, priority):
        self.info = info          # Đối tượng Song
        self.priority = priority  # Độ ưu tiên: Số nhỏ (1, 2,...) được phát trước
        self.next = None

class PriorityQueue:
    def __init__(self):
        self.front = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, song, priority):
        """Chèn và tự động sắp xếp bài hát theo độ ưu tiên tăng dần"""
        new_node = QueueNode(song, priority)
        if self.is_empty() or priority < self.front.priority:
            new_node.next = self.front
            self.front = new_node
        else:
            current = self.front
            while current.next is not None and current.next.priority <= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def dequeue(self):
        """Lấy bài hát có độ ưu tiên cao nhất ở đầu hàng đợi ra"""
        if self.is_empty():
            return None
        tmp = self.front
        self.front = self.front.next
        return tmp.info

    def display_queue(self):
        print("Priority Queue Next:")
        if self.is_empty():
            print("Empty Queue")
        else:
            current = self.front
            while current:
                print(f"   [Queue - Priority {current.priority}] {current.info}")
                current = current.next
        print("=========")

#CONTROLLER (Kết nối Playlist CLL + Stack Lịch sử + Tính năng Shuffle)

class MusicPlayer:
    def __init__(self):
        self.playlist = playList()
        self.history = RecentlyPlayedStack()
        self.queue_next = PriorityQueue()  # Khởi tạo Hàng đợi ưu tiên mới
        self.song_hash_map = {}            # Bảng băm dùng Dictionary để tìm kiếm O(1)
    def quick_search_by_id(self, song_id):
        """Tính năng tìm kiếm sử dụng Bảng băm"""
        # Tra cứu trực tiếp trong dictionary không cần duyệt vòng lặp CLL
        if song_id in self.song_hash_map:
            return self.song_hash_map[song_id]
        return None
    def load_data_from_file(self):
        raw_data = read_file(self.file_path)
        for song_info in raw_data:
            song_obj = Song(song_info[0], song_info[1], song_info[2], song_info[3], song_info[4])
            self.playlist.addSong(song_obj)

    def play_current(self):
        if self.playlist.isEmpty():
            print("No song in playlist.")
            return
        print(f"🎵 Now Playing: {self.playlist.current_track.data}")

    def skip_next(self):
        """Phát bài tiếp theo (CLL) và lưu bài cũ vào Lịch sử (Stack)"""
        if self.playlist.isEmpty():
            return
        old_song = self.playlist.nextSong()
        if old_song:
            self.history.push(old_song) # Đẩy vào Stack lịch sử
        print(f"⏭️ Skipped Next!")
        self.play_current()

    def go_back(self):
        """Quay lại bài trước bằng cách Pop từ Stack lịch sử"""
        if self.history.is_empty():
            print("⏮️ Cannot go back. History is empty!")
            return
        
        # Lấy bài hát vừa nghe từ Stack ra (LIFO)
        previous_song = self.history.pop()
        
        # Tìm và đặt con trỏ phát nhạc về lại bài này trong CLL
        if not self.playlist.isEmpty():
            curr = self.playlist.tail.next
            while True:
                if curr.data.song_id == previous_song.song_id:
                    self.playlist.current_track = curr
                    break
                curr = curr.next
                if curr == self.playlist.tail.next:
                    break
                    
        print(f"⏮️ Went Back to Previous Song!")
        print(f"🎵 Now Playing: {previous_song}")

    def shuffle_play(self):
        """Tính năng Shuffle: Chọn ngẫu nhiên bài hát ngẫu nhiên từ CLL"""
        if self.playlist.isEmpty():
            return
        
        # Gom các nút lại để lấy ngẫu nhiên
        all_nodes = []
        curr = self.playlist.tail.next
        while True:
            all_nodes.append(curr)
            if curr == self.playlist.tail:
                break
            curr = curr.next
            
        random_node = random.choice(all_nodes)
        
        # Lưu bài hiện tại vào lịch sử
        self.history.push(self.playlist.current_track.data)
        # Nhảy con trỏ tới bài ngẫu nhiên
        self.playlist.current_track = random_node
        print(f"🔀 Shuffle Triggered!")
        self.play_current()
    
    def add_new_song(self, song):
        self.playlist.addSong(song)
        write_file(self.file_path, self.playlist)

    def remove_song_by_id(self, song_id):
        removed = self.playlist.removeSong(song_id)
        if removed:
            write_file(self.file_path, self.playlist)
            print(f"--- Successfully removed: {removed} ---")

# MENU CHẠY THỬ

def main():
    player = MusicPlayer()
    player.load_data_from_file()

    while True:
        print("\n=== MUSIC STREAMING PLAYLIST MANAGER ===")
        player.playlist.displayAll()
        player.history.display_history()
        player.play_current()
        
        print("\nSelect an action:")
        print("1. Next Song (Skip Next)")
        print("2. Previous Song (Go Back)")
        print("3. Shuffle Play")
        print("4. Add Song")
        print("5. Remove Song by ID")
        print("0. Exit")
        
        choice = input("Enter choice (0-5): ")
        print("\nOUTPUT:")
        if choice == "1":
            player.skip_next()
        elif choice == "2":
            player.go_back()
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