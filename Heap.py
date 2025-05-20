
class HeapNode:
    def __init__(self, id, priority):
        self.id = id
        self.priority = priority
        self.left = None
        self.right = None
        self.parent = None


class MaxHeap:
    def __init__(self):
        self.root = None
        self.size = 0
        self.nodes = []

    #putting a new node in heap and fix structure
        def insert(self, id, priority):
        new_node = HeapNode(id, priority)
        self.size += 1

        if self.root is None:
            self.root = new_node
            self.nodes.append(new_node)
            return

        p_index = (self.size - 2) // 2
        parent = self.nodes[p_index]
        new_node.parent = parent

        if parent.left is None:
            parent.left = new_node
        else:
            parent.right = new_node

        self.nodes.append(new_node)
        current = new_node
        while current.parent is not None:
            self.maxHeapify(current.parent)
            current = current.parent



    #grab the last node in the heap list
    def find_last_node(self):
        if len(self.nodes) == 0:
            return None
        last_index = len(self.nodes) - 1
        last_node = self.nodes[last_index]
        return last_node

    #delete the max item and max heapify
    def deleteMaxHeap(self):
        if self.root is None:
            return None

        max_id = self.root.id
        max_priority = self.root.priority

        last_node = self.nodes.pop()
        self.size -= 1

        if last_node == self.root:
            self.root = None
            return (max_id, max_priority)

        self.root.id = last_node.id
        self.root.priority = last_node.priority

        if last_node.parent:
            if last_node.parent.right == last_node:
                last_node.parent.right = None
            else:
                last_node.parent.left = None

        self.maxHeapify(self.root)

        return (max_id, max_priority)

    #fix the heap structure after removal
    def maxHeapify(self, node):
        current = node
        biggest = current

        if current.left is not None:
            if current.left.priority > biggest.priority:
                biggest = current.left

        if current.right is not None:
            if current.right.priority > biggest.priority:
                biggest = current.right

        if biggest != current:
            current.id, biggest.id = biggest.id, current.id
            current.priority, biggest.priority = biggest.priority, current.priority
            self.maxHeapify(biggest)

    #just showing whats inside the heap
    def printMaxHeap(self):
        heap_data = []
        index = 0
        for node in self.nodes:
            heap_data.append((node.id, node.priority))
            index += 1
        return heap_data

    #look for a node with same id
    def find_node_by_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    #updating priority of a node if its higher
    def increasePriority(self, id, new_priority):
        node = self.find_node_by_id(id)
        mu = id - 1
        if node is None or new_priority <= node.priority:
            return False
        node.priority = new_priority
        self.bubbleup(node)
        return True

    #remove top priority and delete same from bst
    def processHighestPriorityRequest(self, bst):
        result = self.deleteMaxHeap()
        if result is None:
            return None
        max_id, max_priority = result
        if bst:
            bst.root = bst.deleteRequest(bst.root, max_id)
        return (max_id, max_priority)
