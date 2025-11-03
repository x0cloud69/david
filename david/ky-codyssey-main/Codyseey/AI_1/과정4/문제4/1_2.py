class Node:
    def __init__(self,value):
        self.value = value
        self.next  = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def len(self):
        return self.size
    
    def insert(self,index:int,value:any) -> list:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.size += 1
            return
        current = self.head
        _countOfnode_ = self.len()
        print(_countOfnode_)
        if 0 > index or index > _countOfnode_:
            print("index 범위 에러")
            return 
            #raise ValueError
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            previous = self.head
            for _ in range(index-1):
                previous = previous.next
            new_node.next = previous.next
            previous.next = new_node
        self.size += 1
        
    
    def to_list(self):
        current = self.head
        for i in range(self.size):
          print(f"Node : {self.size}   Value : {current.value}")
          current = current.next 
        
def print_menu():
    print("1. Insert : ")
    print("2. Delete : ")
    print("3. Display : ")
    print("4. Node 수 ")
    print("5. 종료")
        
def main():
    linked = LinkedList()
    while True:
        print_menu()
        _choice_ = input("원하는 작업을 선택 하세요").strip()
        if _choice_ == '1':
            _str_ = input("입력하고자 하는 DATA 입력 : ").strip()
            _pos_ = int(input("삽입하고자 하는 위치를 입력하세요 : ").strip())
            
            if _str_:
               linked.insert(_pos_,_str_)
               linked.to_list()
            
if __name__ == '__main__':
    main()