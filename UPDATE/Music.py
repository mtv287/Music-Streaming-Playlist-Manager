# ==========================================
# 1. CÁC HÀM XỬ LÝ ĐỌC / GHI FILE
# ==========================================

def read_file(file_path):
    """Đọc danh sách bài hát từ file bản ghi txt."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line = file.readline()
        # Chuyển chuỗi đại diện danh sách tuple thành danh sách thật trong Python
        return eval(line.strip()) if line.strip() else []
    except FileNotFoundError:
        # Báo lỗi và trả về danh sách rỗng nếu chưa có file
        print(f"Error: The file '{file_path}' was not found. Creating a new one...")
        return []

def write_file(file_path, playlist_cdll):
    """Lưu danh sách bài hát từ Circular Doubly Linked List vào file txt."""
    try:
        song_list = []
        if not playlist_cdll.isEmpty():
            current = playlist_cdll.head
            # Duyệt qua từng nút trong CDLL để lấy dữ liệu bài hát
            while True:
                song_list.append((
                    current.data.song_id, current.data.title, 
                    current.data.artist, current.data.duration, current.data.genre
                ))
                current = current.next
                if current == playlist_cdll.head:  # Quay lại đầu thì dừng
                    break
        # Ghi chuỗi đại diện dữ liệu vào file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(song_list))
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# ==========================================
# 2. CÁC LỚP CƠ BẢN (Core Classes)
# ==========================================

class Song:
    """Lớp lưu trữ thông tin chi tiết của một bài hát."""
    def __init__(self, song_id=None, title=None, artist=None, duration=None, genre=None):
        self.song_id = song_id      # Mã bài hát (ID)
        self.title = title          # Tên bài hát
        self.artist = artist        # Ca sĩ
        self.duration = duration    # Thời lượng (giây)
        self.genre = genre          # Thể loại nhạc

    def __str__(self):
        # Định dạng chuỗi hiển thị khi in đối tượng Song
        return f"({self.song_id}, {self.title}, {self.artist}, {self.duration}s, {self.genre})"

class songNode: 
    """Nút trong Danh sách liên kết đôi (Doubly Linked Node)."""
    def __init__(self, _data, _next=None, _prev=None):
        self.data = _data   # Dữ liệu chứa đối tượng Song
        self.next = _next   # Con trỏ trỏ đến bài hát tiếp theo
        self.prev = _prev   # Con trỏ trỏ đến bài hát phía trước

# ==========================================
# 3. DANH SÁCH LIÊN KẾT ĐÔI VÒNG (CDLL)
# ==========================================

class CircularDoublyLinkedList: 
    """Quản lý Playlist bằng cấu trúc Danh sách liên kết đôi vòng."""
    def __init__(self):
        self.head = None           # Nút đầu tiên của Playlist
        self.current_track = None  # Con trỏ bài hát đang được chọn phát

    def isEmpty(self):
        """Kiểm tra danh sách có rỗng hay không."""
        return self.head is None

    def addSong(self, new_data):
        """Thêm một bài hát mới vào cuối danh sách."""
        new_node = songNode(new_data)
        if self.isEmpty():
            # Nếu danh sách rỗng, nút mới tự trỏ lại chính nó
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current_track = new_node  # Gán mặc định bài phát đầu tiên
        else:
            tail = self.head.prev  # Nút cuối (tail) trong CDLL luôn là head.prev
            
            # Cập nhật các con trỏ của nút mới
            new_node.next = self.head
            new_node.prev = tail
            
            # Cập nhật liên kết của nút đầu (head) và nút cuối (tail) với nút mới
            tail.next = new_node
            self.head.prev = new_node

    def removeSong(self, song_id):
        """Xóa một bài hát khỏi playlist dựa theo song_id."""
        if self.isEmpty():
            print("Empty!!")
            return None

        current = self.head
        found_node = None

        # 1. Duyệt tìm nút chứa bài hát cần xóa
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

        # 2. Trường hợp danh sách chỉ có đúng 1 bài hát
        if found_node.next == found_node:
            self.head = None
            self.current_track = None
            return found_node.data

        # 3. Nếu bài xóa trùng bài đang phát, chuyển con trỏ sang bài tiếp theo
        if self.current_track == found_node:
            self.current_track = found_node.next

        # 4. Nối con trỏ của nút trước và nút sau để bỏ qua nút bị xóa (Xóa O(1))
        found_node.prev.next = found_node.next
        found_node.next.prev = found_node.prev

        # 5. Cập nhật lại head nếu xóa đúng nút head
        if found_node == self.head:
            self.head = found_node.next

        return found_node.data

    def nextSong(self):
        """Chuyển sang phát bài tiếp theo (Tiến - O(1))."""
        if self.isEmpty() or self.current_track is None:
            return None
        old_song = self.current_track.data
        self.current_track = self.current_track.next  # Đi tới bài tiếp theo
        return old_song

    def prevSong(self):
        """Quay lại bài hát phía trước (Lùi - O(1) nhờ con trỏ prev của CDLL)."""
        if self.isEmpty() or self.current_track is None:
            return None
        self.current_track = self.current_track.prev  # Lùi lại bài phía trước
        return self.current_track.data

    def displayAll(self):
        """Hiển thị toàn bộ các bài hát trong Playlist."""
        if self.isEmpty():
            print("Empty playlist")
            return None
        current = self.head
        while True:
            # Đánh dấu bài đang phát nếu khớp với current_track
            if current == self.current_track:
                marker = " -> [Playing]"
            else:
                marker = ""
            print(f"{current.data}{marker}")
            current = current.next
            if current == self.head:  # Đã duyệt đủ 1 vòng
                break
        print("=========")

# ==========================================
# 4. CẤU TRÚC STACK (Lịch sử nghe nhạc)
# ==========================================

class StackNode:
    """Nút trong Stack."""
    def __init__(self, info):
        self.info = info
        self.next = None

class RecentlyPlayedStack:
    """Quản lý lịch sử nghe nhạc theo cơ chế LIFO (Vào sau ra trước)."""
    def __init__(self):
        self.top = None  # Nút ở đỉnh Stack (bài phát gần nhất)

    def is_empty(self):
        return self.top is None

    def push(self, song):
        """Đẩy bài hát vừa nghe xong vào đỉnh Stack."""
        new_node = StackNode(song)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """Lấy bài hát nghe gần đây nhất ra khỏi Stack."""
        if self.is_empty():
            return None
        tmp = self.top
        self.top = self.top.next
        return tmp.info

    def display_history(self):
        """In toàn bộ lịch sử bài hát đã từng nghe."""
        print("Recently Played History (Stack - LIFO):")
        if self.is_empty():
            print("No history")
        else:
            current = self.top
            while current:
                print(f"   [Past] {current.info}")
                current = current.next
        print("=========")

# ==========================================
# 5. CONTROLLER (Bộ điều khiển trình phát)
# ==========================================

class MusicPlayer:
    """Điều khiển toàn bộ ứng dụng phát nhạc."""
    def __init__(self, file_path="playlist.txt"):
        self.file_path = file_path
        self.playlist = CircularDoublyLinkedList()  # Sử dụng CDLL làm danh sách phát chính
        self.history = RecentlyPlayedStack()        # Sử dụng Stack lưu lịch sử nghe nhạc
        self.song_hash_map = {}                     # Hash Map hỗ trợ tra cứu nhanh O(1)

    def load_data_from_file(self):
        """Nạp dữ liệu từ file lưu trữ vào chương trình."""
        raw_data = read_file(self.file_path)
        for song_info in raw_data:
            song_obj = Song(song_info[0], song_info[1], song_info[2], song_info[3], song_info[4])
            self.playlist.addSong(song_obj)
            self.song_hash_map[song_obj.song_id] = song_obj  # Lưu vào hash map

    def play_current(self):
        """Hiển thị bài hát đang được chọn phát."""
        if self.playlist.isEmpty() or self.playlist.current_track is None:
            print("No song in playlist.")
            return
        print(f"🎵 Now Playing: {self.playlist.current_track.data}")

    def skip_next(self):
        """Bỏ qua bài hiện tại để chuyển sang bài tiếp theo."""
        if self.playlist.isEmpty():
            return
        old_song = self.playlist.nextSong()
        if old_song:
            self.history.push(old_song)  # Lưu bài vừa bỏ qua vào Stack lịch sử
        print(f"⏭️ Skipped Next!")
        self.play_current()

    def go_previous(self):
        """Quay lại bài phát phía trước trực tiếp bằng CDLL."""
        if self.playlist.isEmpty():
            return
        prev_song = self.playlist.prevSong()
        print(f"⏮️ Went Back to Previous Song (CDLL Prev)!")
        print(f"🎵 Now Playing: {prev_song}")

    def shuffle_play(self):
        """Phát ngẫu nhiên một bài hát bất kỳ trong playlist."""
        if self.playlist.isEmpty():
            return
        
        # Gom toàn bộ con trỏ nút vào danh sách tạm
        all_nodes = []
        curr = self.playlist.head
        while True:
            all_nodes.append(curr)
            curr = curr.next
            if curr == self.playlist.head:
                break
            
        # Chọn ngẫu nhiên 1 nút
        random_node = random.choice(all_nodes)
        
        # Lưu bài cũ vào lịch sử trước khi nhảy bài ngẫu nhiên
        if self.playlist.current_track:
            self.history.push(self.playlist.current_track.data)
        
        # Chuyển con trỏ bài phát sang nút ngẫu nhiên được chọn
        self.playlist.current_track = random_node
        print(f"🔀 Shuffle Triggered!")
        self.play_current()
    
    def add_new_song(self, song):
        """Thêm bài hát mới vào chương trình và đồng bộ với file."""
        self.playlist.addSong(song)
        self.song_hash_map[song.song_id] = song
        write_file(self.file_path, self.playlist)

    def remove_song_by_id(self, song_id):
        """Xóa bài hát khỏi chương trình theo ID và đồng bộ với file."""
        removed = self.playlist.removeSong(song_id)
        if removed:
            if song_id in self.song_hash_map:
                del self.song_hash_map[song_id]
            write_file(self.file_path, self.playlist)
            print(f"--- Successfully removed: {removed} ---")

# ==========================================
# 6. GIAO DIỆN VÀ MENU ĐIỀU KHIỂN MAIN
# ==========================================

def main():
    player = MusicPlayer("playlist.txt")
    player.load_data_from_file()  # Tải dữ liệu ban đầu

    while True:
        print("\n=== MUSIC STREAMING PLAYLIST MANAGER (CDLL) ===")
        player.playlist.displayAll()        # Hiển thị playlist CDLL
        player.history.display_history()   # Hiển thị lịch sử nghe
        player.play_current()              # Báo bài đang phát
        
        # In menu tùy chọn
        print("\nSelect an action:")
        print("1. Next Song (Skip Next)")
        print("2. Previous Song (Go Back via CDLL)")
        print("3. Shuffle Play")
        print("4. Add Song")
        print("5. Remove Song by ID")
        print("0. Exit")
        
        choice = input("Enter choice (0-5): ")
        print("\nOUTPUT:")
        
        # Xử lý lựa chọn người dùng
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
