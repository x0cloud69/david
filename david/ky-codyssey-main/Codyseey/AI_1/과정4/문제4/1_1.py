class Node():
    def __init__(self,data):
        self.data = data
        self.next = None
        
class Linkedlist():
    def __init__(self):
        self.head = None
        self.size = 0
        
    def is_empty(self):
        return self.head is None
    
    def get_size(self):
        return self.size
    
    def insert(self,data,position=None):
        new_node = Node(data)
        
        if position is None:
            if self.is_empty():
                self.head = new_node
                self.size += 1
                print(f"Header에 Node 추가 : {data}")
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
                print(f"맨뒤에 Node 추가 : {data}")
            self.size += 1
            return
        if position == 0 :
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            print(f"맨 앞에 추가 : {data}")
            return
        
        if position <0 or position > self.size:
            print(f"유효하지 않은 위치 입니다.")
        
        #중간 위치에 상빕
        current = self.head
        for i in range(position -1 ):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        print(f"Node 추가 위치 {position} 노드 내용 : {data} ")
        
    def delete(self,data):
        if self.is_empty():
            print("리스트가 없습니다")
            return
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            print(f"{data} 삭제 완료")
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                print(f"{data} 삭제완료")
                return True
        print(f" '{data}'를 찾을 수 없습니다")
        
    def search(self,data):
        if self.is_empty():
            print(f"리스트가 비어 있습니다.")
            return 
        current = self.head
        position = 0
        
        while current.next:
            if current.data == data:
                print(f"Data : {data}, 위치 : {position}")
                return position
            current = current.next
            position += 1
        print(f" {data}을 찾을 수 없습니다")
        return -1
    def display(self):
        if self.is_empty():
            print(f" 리스트가 비어있습니다")
            return -1
        print("===== Play List =====")
        current = self.head
        position = 0
        
        while current:
            print(f" {position} :  {current.data}")
            current = current.next
            position += 1
        print("="*60)

def print_menu():
    print("\n" + "=" * 60)
    print("1. 음악 추가 (맨뒤)")
    print("2. 음악 추가 (맨앞)")
    print("3. 음악 추가 (특정 위치)")
    print("4. 음악 삭제") 
    print("5. Play List 보기")
    print("0. 종료")
    print("="* 60)
    
if __name__ == '__main__':
    playlist = Linkedlist()
    while True:
        print_menu()
        choice = input("선택 하세요 : ").strip()
        if choice == '1':
            _data_ = input("추가할 노래 제목을 입력하세요").strip()
            if _data_:
                playlist.insert(_data_)
                playlist.display()
            else:
                print("음악 제목을 입력하세요")
        if choice == '2':
            _data_=input("추가할 노래 제목을 입력하세요").strip()  
            if _data_:
                playlist.insert(_data_,0)
                playlist.display()
            else:
                print(f"음악 제목을 입력하세요")
        if choice == '3':
            _data_=input("추가할 노레 제목을 입력하세요").strip()
            _pos_ =int(input("삽입할 위치를 입력하세요"))
            playlist.insert(_data_,_pos_)
            playlist.display()
        if choice == '4':
            _data_=input("삭제할 노래 제목을 입력하세요").strip()
            if _data_:
                playlist.delete(_data_)
                playlist.display()
            else:
                print("음악 제목을 입력하세요")
        if choice == '5':
            playlist.display()
        if choice == '0':
            break
                  
    
    
            