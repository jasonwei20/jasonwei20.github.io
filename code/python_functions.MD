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
    
    def insert_element(self, element):  # Insert in binary tree.
        if self.data == None:
            self.data = element
        else:
            if element < self.data:
                if self.left == None:
                    self.left = Node(element)
                else:
                    self.left.insert_element(element)
            elif element > self.data:
                if self.right == None:
                    self.right = Node(element)
                else:
                    self.right.insert_element(element)
    
    def target_in_tree(self, target):  # Only works for binary search tree.
        if self.data == target:
            return True
        elif target < self.data:
            if self.left is not None:
                return self.left.target_in_tree(target)
        elif target > self.data:
            if self.right is not None:
                return self.right.target_in_tree(target)
        return False
    
    def print_in_order(self):
        if self != None:
            if self.left != None:
                self.left.print_in_order()
            print(self.data)
            if self.right:
                self.right.print_in_order()
```
