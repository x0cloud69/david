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

def menu():
    print("=================================")
    print("0. 종료")
    print("1. (단순) Node 삽입")
    print("2. (단순) Node 삭제")
    print("3. (단순) Node 조회")
    print("4. (단순) Node 갯수")
    print("=================================")

class Node:    
   def __init__(self,value):
       self.value = value
       self.next  = None

class Linklist: 
    def __init__(self):
        self.head = None
        self.size = 0
        
    def insert(self,index:int,value:any) ->None:
        if self.size < index:
            raise ValueError
        
        new_node = Node(value)
        if index == 0:
            self.head = new_node
            self.size += 1
        else:
            _current_ = self.head
            for _ in range(index-1):
                _current_.next = _current_.next.next
            _current_.next = new_node
            new_node.next = _current_.next.next
            self.size += 1 
            
    def to_list(self) -> list:
        _answer_ = []
        _current_ = self.head
        for _ in range(self.size):
            _answer_.append(_current_.value)
            if _current_.next != None:
               _current_ = _current_.next
        print(_answer_)
            
def main():
    
    ll = Linklist()
    
    while True:
        menu()
        try:
            _num_ = input("원하는 작업을 선택 하세요 : ").strip()
            if _num_ == '0':
                return
            if _num_ == '1':
                _input_ = int(input("삽입하고자 하는 위치를 등록 하세요 : ").strip())
                _value_ = input("등록하고자 하는 값을 등록 하세요 : "). strip()
                
                ll.insert(_input_,_value_) 
            if _num_ == '3':
                ll.to_list()
        except ValueError:
            print("indexError") 
            return       
            

if __name__ == '__main__':
    main()