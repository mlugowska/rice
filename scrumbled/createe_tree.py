# Python program to construct tree using in_order and
# pre_order traversals

# A binary tree node
class Node:

    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


"""Recursive function to construct binary of size len from
   in_order traversal in[] and pre_order traversal pre[].  Initial values
   of pre_strt and in_end should be 0 and len -1.  The function doesn't
   do any error checking for cases where in_order and pre_order
   do not form a tree """


def build_tree(in_order, pre_order, pre_strt, in_end):
    if pre_strt > in_end:
        return None

    # Pick current node from pre_order traversal using
    # pre_index and increment pre_index
    t_node = Node(pre_order[build_tree.pre_index])
    build_tree.pre_index += 1

    # If this node has no children then return
    if pre_strt == in_end:
        return t_node

    # Else find the index of this node in in_order traversal
    inIndex = search(in_order, pre_strt, in_end, t_node.data)

    # Using index in in_order Traversal, construct left
    # and right subtrees
    t_node.left = build_tree(in_order, pre_order, pre_strt, inIndex - 1)
    t_node.right = build_tree(in_order, pre_order, inIndex + 1, in_end)

    return t_node


# UTILITY FUNCTIONS
# Function to find index of value in arr[start...end]
# The function assumes that value is present in in_order[]

def search(arr, start, end, value):
    for i in range(start, end + 1):
        if arr[i] == value:
            return i


def print_in_order(node):
    if node is None:
        return

    # first recur on left child
    print_in_order(node.left)

    # then print the data of node
    print(node.data, end=' ')

    # now recur on right child
    print_in_order(node.right)


# Driver program to test above function
in_order = ['M', 'L', 'K', 'A', 'E', 'D', 'C', 'B', 'J', 'I', 'H', 'G', 'F', 'X', 'R', 'Q', 'P', 'O', 'N']
pre_order = ['A', 'B', 'D', 'E', 'C', 'F']
# Static variable pre_index
build_tree.pre_index = 0
root = build_tree(in_order, pre_order, 0, len(in_order) - 1)

# Let us test the build tree by printing in_order traversal
print("in_order traversal of the constructed tree is")
print_in_order(root)