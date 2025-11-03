class Node:
    def __init__(self,data):
         self.data = data
         self.next = None

class SingleLinkedList:
     def __init__(self):
        self.head = None

     def addNode(self, data):
         new_node = Node(data)

         if self.head is None:
            self.head = new_node
            return

         current = self.head
         while  current.next is not None:
            current = current.next

         current.next = new_node

my_list = SingleLinkedList()

my_list.addNode(10)
my_list.addNode(20)
my_list.addNode(30)

print("첫번째 Node :",my_list.head.data)
print("첫번째 Node의 Next  :",my_list.head.next)
print("두번째 Node :",my_list.head.next.data)
print("두번째 Node의 Next :",my_list.head.next.next)
print("세번째 Node :",my_list.head.next.next.data)
print("세번째 Node의 Next :",my_list.head.next.next.next)

