"""File: linkedbst.py Author: Ken Lambert."""

import random
import timeit

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the contents of
        sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated 90 degrees
        counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the matched item, or None
        otherwise."""

        def recurse(node):
            # if node is None:
            #     return None
            # elif item == node.data:
            #     return node.data
            # elif item < node.data:
            #     return recurse(node.left)
            # else:
            #     return recurse(node.right)
            while node is not None:
                if item == node.data:
                    return node.data
                if item < node.data:
                    node = node.left
                else:
                    node = node.right
            return None

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            # if item < node.data:
            #     if node.left is None:
            #         node.left = BSTNode(item)
            #     else:
            #         recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            # elif node.right is None:
            #     node.right = BSTNode(item)
            # else:
            #     recurse(node.right)
            # End of recurse
            while node is not None:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        return
                    node = node.left
                else:
                    if node.right is None:
                        node.right = BSTNode(item)
                        return
                    node = node.right

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.

        Raises: KeyError if item is not in self.
        postcondition: item is removed from self.
        """
        if item not in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while currentNode.right is not None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = "L"
        currentNode = self._root
        while currentNode is not None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = "L"
                currentNode = currentNode.left
            else:
                direction = "R"
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if currentNode.left is not None and currentNode.right is not None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:
            # Case 2: The node has no left child
            if currentNode.left is None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """If item is in self, replaces it with newItem and returns the old item, or
        returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """Return the height of tree :return: int."""

        def height1(top):
            """Helper function :param top:

            :return:
            """
            if top is None:
                return -1
            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        """Return True if tree is balanced :return:"""

        def min_height(top):
            """Helper function :param top:

            :return:
            """
            if top is None:
                return -1
            return 1 + min(min_height(top.left), min_height(top.right))

        return self.height() - min_height(self._root) <= 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [item for item in self if low <= item <= high]

    def rebalance(self):
        """Rebalances the tree.

        :return:
        """
        items = [item for item in self]
        self.clear()
        self._rebalance_helper(items, 0, len(items) - 1)

    def _rebalance_helper(self, items, low, high):
        """Helper function for rebalance.

        :param items: 
        :param low: 
        :param high: 
        :return:
        """
        if low <= high:
            mid = (low + high) // 2
            self.add(items[mid])
            self._rebalance_helper(items, low, mid - 1)
            self._rebalance_helper(items, mid + 1, high)

    def successor(self, item):
        """Returns the smallest item that is larger than item, or None if there is no
        such item.

        :param item: 
        :type item: 
        :return: 
        :rtype:
        """
        successor = None
        for i in self:
            if i > item:
                successor = i
                break

        if successor is None:
            return None

        for i in self:
            if i > item and i < successor:
                successor = i

        return successor

    def predecessor(self, item):
        """Returns the largest item that is smaller than item, or None if there is no
        such item.

        :param item: 
        :type item: 
        :return: 
        :rtype:
        """
        predecessor = None
        for i in self:
            if i < item:
                predecessor = i
                break

        if predecessor is None:
            return None

        for i in self:
            if i < item and i > predecessor:
                predecessor = i

        return predecessor

    def demo_bst(self, path):
        """Demonstration of efficiency binary search tree for the search tasks.

        :param path: 
        :type path: 
        :return: 
        :rtype:
        """
        NUMBER_OF_TRIES = 10000
        time_open = timeit.default_timer()
        with open(path, "r") as f:
            dictionary = f.read().splitlines()

        time_open = timeit.default_timer() - time_open
        print("Time to read file: ", time_open)

        random_words = random.choices(dictionary, k=NUMBER_OF_TRIES)

        self.clear()
        time_bst_create = timeit.default_timer()
        for word in dictionary:
            self.add(word)
        time_bst_create = timeit.default_timer() - time_bst_create

        print("Time to create bst: ", time_bst_create)

        time_find_list = 0
        for word in random_words:
            start = timeit.default_timer()
            dictionary.index(word)
            end = timeit.default_timer()
            time_find_list += end - start

        print("Time for find in list: ", time_find_list)

        time_find_bst_alphabet = 0
        for word in random_words:
            start = timeit.default_timer()
            self.find(word)
            end = timeit.default_timer()
            time_find_bst_alphabet += end - start

        print("Time for find in bst alphabetically: ", time_find_bst_alphabet)

        self.clear()
        time_bst_create = timeit.default_timer()
        for _ in range(NUMBER_OF_TRIES):
            self.add(random.choice(dictionary))
        time_bst_create = timeit.default_timer() - time_bst_create

        print("Time to create bst random: ", time_bst_create)

        time_find_bst_random = 0
        for word in random_words:
            start = timeit.default_timer()
            self.find(word)
            end = timeit.default_timer()
            time_find_bst_random += end - start

        print("Time for find in bst random: ", time_find_bst_random)

        time_find_bst_balanced = timeit.default_timer()
        self.rebalance()
        time_find_bst_balanced = timeit.default_timer() - time_find_bst_balanced

        print("Time to rebalance bst: ", time_find_bst_balanced)

        time_find_bst_balanced = 0
        for word in random_words:
            start = timeit.default_timer()
            self.find(word)
            end = timeit.default_timer()
            time_find_bst_balanced += end - start

        print("Time for find in bst balanced: ", time_find_bst_balanced)

        return (
            time_find_list,
            time_find_bst_alphabet,
            time_find_bst_random,
            time_find_bst_balanced,
        )
