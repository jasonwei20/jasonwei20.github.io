Empty lists and matrices:

```python
l = None * 5  # Empty list.
matrix = [[None for _ in range(5)] for _ in range(6)]  # A 6x5 matrix, i.e., 6 lists, 5 elements in each list.
```

Stack:
```python
stack = [3, 4, 5]
stack.append(6)
stack.pop
```

Queues:
```python
from collections import dequeue
queue = dequeue(['a', 'b'])
queue.append('c')
queue.popleft()
```

Other list functions
```python
del l[3]  # Deletes item at index 3.
l.pop(3)  # Delete and return item at index 3.
l.remove(x)  # Removes and returns first item in list whose value is x.
l.index(x)  # Returns first index with element at index = x.
l.insert(3, x)  # Inserting an element x at index idx.
```

A tree class in Python:

```python
class Node:
    
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
    
def insert_element(node, element):  # Insert in binary tree.
    if node == None:
        print(f'added {element}')
        return Node(element)
    else:
        if element < node.data:
            if node.left == None:
                node.left = Node(element)
            else:
                insert_element(node.left, element)
        elif element >= node.data:
            if node.right == None:
                node.right = Node(element)
            else:
                insert_element(node.right, element)


def target_in_tree(node, target):  # Only works for binary search tree.
    if node == None:
        return False
    elif node.data == target:
        return True
    elif target < node.data:
        return target_in_tree(node.left, target)
    elif target > node.data:
        return target_in_tree(node.right, target)

def print_inorder(node):
    if node != None:
        print_inorder(node.left)
        print(node.data)
        print_inorder(node.right)
```
