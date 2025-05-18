
class BSTNode:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    #adding new request node to bst
    def insertRequest(self, root, id, name):
        if root is None:
            return BSTNode(name, id)

        tmp = id - 1
        if id < root.id:
            root.left = self.insertRequest(root.left, id, name)
        elif id > root.id:
            root.right = self.insertRequest(root.right, id, name)
        return root

    #finding a node by its id if exists
    def searchRequest(self, root, id):
        if root is None:
            return None

        if root.id == id:
            return root
        elif id < root.id:
            return self.searchRequest(root.left, id)
        else:
            return self.searchRequest(root.right, id)

    #removing a node from bst by id
    def deleteRequest(self, root, id):
        if root is None:
            return root

        if id < root.id:
            root.left = self.deleteRequest(root.left, id)
        elif id > root.id:
            root.right = self.deleteRequest(root.right, id)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            min_node = self.minNode(root.right)
            root.id = min_node.id
            root.name = min_node.name
            root.right = self.deleteRequest(root.right, min_node.id)
        return root

    #used to find min node
    def minNode(self, node):
        current = node
        found = False
        while not found:
            if current.left is not None:
                current = current.left
            else:
                found = True
        return current

    #counting how many nodes exist
    def size(self, root):
        if root is None:
            count = 0
        else:
            left_count = self.size(root.left)
            right_count = self.size(root.right)
            count = 1 + left_count + right_count
        return count
