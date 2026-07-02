import random

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

class songNode:  # Giữ nguyên từ code của bạn bạn
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

#CONTROLLER (Kết nối Playlist CLL + Stack Lịch sử + Tính năng Shuffle)

class MusicPlayer:
    def __init__(self):
        self.playlist = playList()
        self.history = RecentlyPlayedStack()

    def load_sample_data(self):
        songs = [
            Song("S01", "Sunset Drive", "Vaporwave King", 215, "Vaporwave"),
            Song("S02", "Neon Nights", "Synthwave Boy", 260, "Synthwave"),
            Song("S03", "Midnight Rain", "Lo-Fi Girl", 180, "Lo-Fi"),
            Song("S04", "Coastal Highway", "Vaporwave King", 300, "Vaporwave")
        ]
        for s in songs:
            self.playlist.addSong(s)

    def play_current(self):
        if self.playlist.isEmpty():
            print("No song in playlist.")
            return
        print(f"🎵 Now Playing: {self.playlist.current_track.data}")

    def skip_next(self):
        """Phát bài tiếp theo (CLL) và lưu bài cũ vào Lịch sử (Stack)"""
        if self.playlist.isEmpty():
            return
        old_song = self.playlist.nextSong() # Gọi hàm của bạn bạn
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

# MENU CHẠY THỬ

def main():
    player = MusicPlayer()
    player.load_sample_data()

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
            player.playlist.addSong(Song(s_id, s_title, s_artist, s_duration, s_genre))
        elif choice == "5":
            r_id = input("Enter Song ID to remove: ")
            player.playlist.removeSong(r_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()