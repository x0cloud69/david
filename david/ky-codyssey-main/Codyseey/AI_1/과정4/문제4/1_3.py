"""
단순리스트 : 임의 위치 삽입/삭제 와 리스트 반환
insert(self,index:int,value:any) ->None:  0 <= index <= len  indexError 발생
delete(self,index:int) -> objext : 해당 위치 노드 삭제후 삭제된 값 반환 
                                   해당 위치 없으면 indexError
to_list(self) -> list : 앞 뒤 순서의 값
_len_(self): 노드수 반환환
"""

"""
insert(self,value:any): 
  비어 있으면 단일로드 원형구성 , 아니면 커서 뒤에 삽입후 커서를 새노드로 이동

delete(self,value:any)->bool : 
  값이 같은 첫노드 삭제(성공:True, 없음:False)
  삭제노드가 커서면 커서를 이전노드로 이동
  노드 1개만 있고 삭제되면, 빈 상태

get_next(self)->object|None:
   비었으면 None, 아니면, 커서를 다음노드로 이동 후 그 값을 반환(순환)

search(self,value:any)->bool: 
   존재 여부 확인 

"""
class Node:
    def __init__(self,value):
        self.value = value
        self.next  = None
        
class Linkedlist:
    def __init__(self):
        self.head = None
        self.size = 0
        
    #노드 수 return
    def __len__(self):
        return self.size
    
    #노드 Display 
    def to_list(self):
        current = self.head
        _pos_   = 0 
        answer = []
        while current:
            answer.append(current.value)
            current = current.next
        return answer
        
    # Insert Node
    def insert(self,index,value):
        if index < 0 or index > self.size:
            raise IndexError("IndexError")
        current = self.head
        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index-1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.size += 1
        return 
        
    def delete(self,index:int) -> object:
        if 0 > index or index >= self.size :
            raise IndexError
        current = self.head
        if index == 0:
                _del_ = current.value
                self.head = current.next
        else:
            for _ in range(index-1):
                current = current.next
            _del_ = current.next.value
            current.next = current.next.next
        self.size -= 1
        return _del_
    
# 원형 List    
class Circlelist:
    def __init__(self):
        self.head = None
        self.size = 0
        self.cursor = None
    
    def insert(self,value:any):
       # current = self.head
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.size += 1
            self.cursor = new_node
            new_node.next = self.head
        else:
            new_node.next = self.cursor.next
            self.cursor.next = new_node
            self.cursor = new_node
            self.size += 1
            
    def get_next(self):
        if self.head == None:
            return None
        _answer_ = []
        current = self.cursor.next
        for _ in range(self.size):
            _value_ = current.value
            _answer_.append(_value_)
            current = current.next
        self.cursor = current

        return _answer_        
        
        
    def search(self,value:any)->bool:
        _answer_ = False
        current = self.head
        for _ in range(self.size): 
            if current.value == value:
                return True
            current = current.next
            # self.cursor = self.cursor.next
                
        return False      
    
    def delete(self,value:any)->bool:
        if self.head == None:
            return None
        prev = self.head
        target = self.head
        _answer_  = False
        for _ in range(self.size -1):
            prev = prev.next
            
        for _ in range(self.size):
            if target.value == value:
               if self.size == 1:
                   self.head = None
                   self.cursor = None
               else:
                   prev.next = target.next
                   if target is self.head:
                       self.head = target.next
                   if target is self.cursor:
                       self.cursor = prev
               self.size -= 1
               return True
            prev = target
            target = target.next
        return False
                   
            
def menu():
    print("===========================")
    print("| 1. (단일) Node 생성      |") 
    print("| 2. (단일) Node 삭제      |")
    print("| 3. (단일) Node 조회      |")   
    print("| 4. (단일) Node 수        |")
    print("| 5. (원형) Node 생성      |")
    print("| 6. (원형) Node 삭제      |")
    print("| 7. (원형) Node Get Next  |")
    print("| 8. (원형) Search         |")
    print("| 0. 종료                  |")
    print("======================= ====")     
                
def main():
    ll = Linkedlist()
    cl = Circlelist()
    
    while True:
       menu()
       _num_ = input("원하는 작업 번호를 선택하세요 : ")
       if _num_ == '0':
          break
       try:       
            if _num_ == '1':
                _value_ = input("추가하고자 하는 값을 등록 하세요.")
                _index_ = int(input("추가하고자 하는 위치를 등록하세요."))
                ll.insert(_index_,_value_) 
            elif _num_ == '2':
                _position_ = int(input("삭제하고자 하는 위치를 등록하세요 : "))
                print(f"삭제된 Node : {ll.delete(_position_)}")
            elif _num_ == '3':   
                _answer_ = ll.to_list()
                print(_answer_)
            elif _num_ == '4':
                print(len(ll))
            elif _num_ == '5':
                _value_ = input("추가 하고자 하는 값을 등록하세요 : ")
                cl.insert(_value_)
            elif _num_ == '6':
                _value_ = input("삭제 하고자 하는 값을 등록하세요 : ")
                _result_ = cl.delete(_value_)
                print(_result_)
            elif _num_ == '7':
                _result_ = cl.get_next()
                print(_result_)      
            elif _num_ == '8':
                _value_ = input("찾고자 하는 값을 입력 하세요 : ").strip()
                _result_ = cl.search(_value_)      
                print(_result_)   
            else:
                print("잘못된 번호 입니다다")
       except (IndexError,ValueError):
            print("IndexError")     
            

    
    
if __name__ == '__main__':
    main()
    