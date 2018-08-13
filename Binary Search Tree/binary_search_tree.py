class TreeNode(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class BinarySearchTree(object):
    def __init__(self, tree_data): 
        self.tree = TreeNode(tree_data[0])
        for x in tree_data[1:]:
            node = self.tree
            while True:
                if node.data >= x:
                    if node.left:
                        node = node.left
                    else:
                        node.left = TreeNode(x)
                        break
                else:
                    if node.right:
                        node = node.right
                    else:
                        node.right = TreeNode(x)
                        break

    def data(self):
        return self.tree

    def sorted_data(self, parent=-1):
        if not parent:
            return []
        if parent == -1:
            parent = self.tree
        return [*self.sorted_data(parent.left), parent.data, *self.sorted_data(parent.right)]