class Song:
    def __init__(self,_id,_title,_artist,_duration,_genre):
        self.id = _id
        self.artist = _artist
        self.title = _title
        self.duration = _duration
        self.genre = _genre
    def display(self):
        print(f"{self.id},{self.artist},{self.title},{self.duration},{self.genre}")

class SongNode:
    def __init__(self,_data,_next):
        self.data = _data
        self.next = _next
    def display(self):
        self.data.display()

class playList:
    def __init__(self):
        self.tail=None
    def isEmpty(self):
        return self.tail==None
    def addSong(self,new_data):
        new_node=SongNode(new_data,None)
        if self.isEmpty():
            self.tail=new_node
            new_node.next=new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node
    def removeSong(self,song):
        if self.isEmpty():
            print("Empty!!")
            return 
        elif self.tail == self.tail.next:
            if self.tail.data == song:
                valueSong = self.tail
                self.tail = None
                return valueSong
            else:
                print("no song match")
                return None
        else:
            current=self.tail.next
            prev=self.tail
            while True:
                if current.data==song:
                    valueSong=current
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
        if self.isEmpty():
            return None
        else:
            self.tail=self.tail.next
            return self.tail.data
    def displayAll(self):
        if self.isEmpty():
            return None
        current=self.tail.next
        while True:
            print(current.data)
            if current==self.tail:
                break
            current=current.next
def testcase():
    pass
if __name__=='__main__':
    testcase()