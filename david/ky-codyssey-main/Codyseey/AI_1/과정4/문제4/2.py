class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def insert(self, data, position=None):
        new_node = Node(data)
        
        # 비어있는 경우
        if self.is_empty():
            self.head = new_node
            new_node.next = self.head  # 원형으로 만들기
            self.size += 1
            print(f"첫 번째 노드 추가 : {data}")
            return
        
        # 맨 뒤에 추가 (position이 None인 경우)
        if position == None:
            current = self.head
            while current.next != self.head:  # head로 돌아올 때까지
                current = current.next
            current.next = new_node
            new_node.next = self.head  # 원형 연결
            print(f"Node 맨뒤에 추가 : {data}")
            self.size += 1
            return
        
        # 맨 앞에 추가 (position == 0)
        if position == 0:
            # 먼저 마지막 노드를 찾아서 new_node를 연결
            current = self.head
            while current.next != self.head:
                current = current.next
            # current는 마지막 노드
            new_node.next = self.head
            self.head = new_node
            current.next = self.head  # 마지막 노드가 새 head를 가리킴
            self.size += 1
            print(f"맨앞에 추가 : {data}")
            return
        
        # 유효한 position 범위 확인
        if position < 0 or position > self.size:
            print(f"유효하지 않은 위치 입니다. (0 ~ {self.size} 사이의 값이어야 합니다.)")
            return
        
        # 중간 위치에 삽입
        current = self.head
        for i in range(position - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        print(f" '{data}' 위치  {position}에 추가 완료")
        
    def delete(self, data):
        if self.is_empty():
            print("리스트가 비어 있습니다.")
            return
        
        # 첫번째 노드를 삭제하는 경우
        if self.head.data == data:
            if self.size == 1:  # 노드가 1개만 있는 경우
                self.head = None
                self.size = 0
                print(f"'{data}' 삭제 완료")
                return True
            else:
                # 마지막 노드를 찾아서 연결
                current = self.head
                while current.next != self.head:
                    current = current.next
                # current는 마지막 노드
                self.head = self.head.next
                current.next = self.head
                self.size -= 1
                print(f"'{data}' 삭제 완료")
                return True
        
        # 중간 또는 마지막 노드 삭제
        current = self.head
        while current.next != self.head:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                print(f"'{data}' 삭제 완료")
                return True
            current = current.next
        
        print(f" '{data}' 를 찾을 수 없습니다.")
        return False
    
    def search(self, title):
        if self.is_empty():
            print(f"리스트가 없습니다")
            return -1
        
        current = self.head
        position = 0
        
        while True:
            if current.data == title:
                print(f" 제목 : {title}  위치 : {position} 번째")
                return position
            current = current.next
            position += 1
            if current == self.head:  # 한 바퀴 돌았으면
                break
        
        print(f" {title}을 찾을 수 없습니다.")
        return -1
    
    def display(self):
        if self.is_empty():
            print(f"리스트가 비어 있습니다.")
            return
        
        print("============ 현재 Play List =============")
        current = self.head
        position = 0
        
        while True:
            print(f"     {position},    {current.data}  size : {self.size}")
            current = current.next
            position += 1
            if current == self.head:  # 원형이므로 head로 돌아오면 멈춤
                break
        print("="*50)
    
    def get_at(self, position):
        if position < 0 or position >= self.size:
            print(f"유효 하지 않는 위치 입니다")
            return None
        
        current = self.head
        for i in range(position):
            current = current.next
        return current.data
     
    def clear(self):
        self.head = None
        self.size = 0
        print("Play List 가 초기화 되었습니다.")
    
    def get_size(self):
        return self.size

def print_menu():
    print("\n" + "="*60)
    print("음악 플레이 리스트 관리 시스템")
    print("=" * 60)   
    print("1. 음악 추가 (맨 뒤)")
    print("2. 음악 추가 (맨 앞)")
    print("3. 음악 추가 (특정 위치)")
    print("4. 음악 삭제")
    print("5. 음악 검색")
    print("6. 플레이리스트 보기")
    print("7. 플레이리스트 초기화")
    print("0. 종료")
    print("=" * 60)
    
if __name__ == '__main__':
    playlist = CircularLinkedList()
    
    while True:
        print_menu()
        choice = input("선택 하세요 : ").strip()
        if choice == '1':
            title = input("추가할 음악 제목을 입력하세요 . ").strip()
            if title:
                playlist.insert(title)
                playlist.display()
            else:
                print("음악 제목을 입력하세요")
        elif choice == '2':
            title = input("추가할 음악 제목을 입력하세요 .").strip()
            if title:
                playlist.insert(title,0)
                playlist.display()
            else:
                print("음악 제목을 입력하세요")
        elif choice == '3':
            title = input("추가할 음악 제목을 입력하세요 : ")
            if not title:
                print("음악 제목을 입력하세요")
                continue
            try:
                position = int(input(f"삽입할 위치를 입력하세요"))
                playlist.insert(title,position)
                playlist.display()
            except ValueError:
                print("숫자를 입력하세요")
        elif choice == '4':
            title = input("삭제할 음악 제목을 입력하세요 : ")
            if title:
                playlist.delete(title)
                playlist.display()
            else:
                print("음악 제목을 입력하세요")
        elif choice == '5':
            title = input("검색할 음악 제목을 입력히세요")
            if title:
                playlist.search(title)
            else:
                print("음악 제목을 입력하세요")
        elif choice == '6':
            playlist.display()
        elif choice == '7':
            confirm = input("정말로 플레이 리스트를 초기화 하겠습니까 (y/n) : ")
            if confirm.lower() == 'y':
                playlist.clear()
                print("플레이 리스트가 초기화 되었습니다")
            else:
                print("초기화가 취소 되었습니다.")
        elif choice == '0':
            print("프로그램이 종료되었습니다.")
            break
        else:
            print("잘못된 선택 입니다.")        
            
        

    
