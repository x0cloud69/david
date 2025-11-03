class Node:
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
        
    
class binarytree:
    def __init__(self):
        self.root = None
        
    def insert(self,data):
        if self.root is None:
            self.root = Node(data)
        else:
            self.insert_recursive(self.root,data)
            
    def insert_recursive(self,current_node,data):
        if data < current_node.data:
            # 추가 하려는 노드가 현재 노드 값보다 작으면
            if current_node.left is None:
                current_node.left = Node(data)
            else:
                self.insert_recursive(current_node.left,data)
        elif data > current_node.data:
            if current_node.right is None:
                current_node.right = Node(data)
            else:
                self.insert_recursive(current_node.right,data)
                
    def find(self,data):
        return self.find_recursive(self.root,data)
    
    def find_recursive(self,current_node,data):
        if current_node is None:
            return False
        if current_node.data == data:
            return True
        
        if data < current_node.data:
            return self.find_recursive(current_node.left,data)
        else:
            return self.find_recursive(current_node.right,data)
        
    def delete(self,data):
        self.root = self.delete_recursive(self.root,data)
        
    def delete_recursive(self,current_node,data):
        if current_node is None:
            return current_node
        
        if data < current_node.data:
            current_node.left = self.delete_recursive(current_node.left,data)
        elif data > current_node.data:
            current_node.right = self.delete_recursive(current_node.right,data)
        else:
            if current_node.left is None and current_node.right is None:
                return None
            elif current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            else:
                min_node = self.find_min_node(current_node.right)
                current_node.data = min_node.data
                current_node.right = self.delete_recursive(current_node.right,min_node.data)
        return current_node
    
    def find_min_node(self,node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def inorder_traversal(self):
        result = []
        self.inorder_recursive(self.root,result)
        return result
    
    def inorder_recursive(self,node,result):
        if node:
            self.inorder_recursive(node.left,result)
            result.append(node.data)
            self.inorder_recursive(node.right,result)
            
bst = binarytree()

print("--- 원소 추가 ----")
elements = [50,30,70,20,40,60,80]

for e1 in elements:
    bst.insert(e1)
    print(f"{e1} 추가됨")
    
print("\n 현재 트리 (중위순회) : " , bst.inorder_traversal())

print("\n -- 원소 탐색")
print("값 40 찾기 : ",bst.find(40))
print("값 90 찾기 : ",bst.find(90))

print("\n--- 원소 삭제---")
bst.delete(20)
print("리프 노드 20 삭제 후 :", bst.inorder_traversal())

# 자식이 하나인 노드 삭제
bst.delete(30)
print("자식이 하니인 노드 30 삭제 후 : ", bst.inorder_traversal())

# 자식이 둘인 노드 삭제
bst.delete(50)
print("자식이 둘인 노드 50 삭제 후 : ", bst.inorder_traversal())    