"""
File: linkedbst.py
Author: Ken Lambert
"""
import sys
sys.setrecursionlimit(100000)
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
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
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
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
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

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
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

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
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
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
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
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
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            if top == None:
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def dfs(v):
            if v == None: return 0
            return 1 + dfs(v.left) + dfs(v.right)
        n = dfs(self._root)
        return self.height() < 2 * log(2 * (n + 1)) - 1
        
    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        ans = []
        lst = []
        lst.append(self._root)
        while len(lst) > 0:
            v = lst[-1]
            lst.pop()
            if v == None:
                continue
            if low <= v.data and v.data <= high:
                ans.append(v.data)
            lst.append(v.left)
            lst.append(v.right)
        ans.sort()
        return ans

    def rebalance(self):

        '''
        Rebalances the tree.
        :return:
        '''
        items = list(self.inorder())
        items.sort()
        self.clear()

        def rec(xd):
            if not xd:
                return None
            m = len(xd) // 2
            l = rec(xd[:m])
            r = rec(xd[m + 1:])
            return BSTNode(xd[m], l, r)
        self._size = len(items)
        self._root = rec(items)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def gt(v, x):
            if v == None:
                return None
            if v.data > x:
                z = gt(v.left, x)
                if z == None:
                    return v.data
                return z
            else:
                z = gt(v.right, x)
                return z
        return gt(self._root, item)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        
        def gt(v, x):
            if v == None:
                return None
            if v.data < x:
                z = gt(v.right, x)
                if z == None:
                    return v.data
                return z
            else:
                z = gt(v.left, x)
                return z
        return gt(self._root, item)
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        mx = 10000
        f = open(path, 'r')
        wrds = []
        for l in f:
            wrds.append(l)
        selected = random.sample(wrds, mx)
        st = time.time()
        for i in selected:
            wrds.index(i)
        en = time.time()
        print(f"Time to search {mx} sample in all words in built-in list: {en-st}")

        """
        We could not manage to add items in this order, because tree depth would be linear, and whole find function would take n^2 time, so program will never execute. 
        So, we will only try to build tree and test on really small sample. 
        """
        print("TESTING NAIVE ADDITION WITH 1000 WORDS")
        mn = 1000
        st = time.time()
        for i in wrds[:mn]:
           self.add(i)
        en = time.time()
        print(f"Time to build binary tree containing all words in sorted order: {en - st}")

        
        st = time.time()
        for i in wrds[:mn]:
            assert (self.find(i) != None)
        en = time.time()
        print(f"Time to search sample in given binary tree: {en - st}")

        self.clear()

        print("Testing with random permutation of words")
        random.shuffle(wrds)
        st = time.time()
        for i in wrds:
           self.add(i)
        en = time.time()
        print(f"Time to build binary tree containing all words in random order: {en - st}")

        
        st = time.time()
        for i in selected:
            assert (self.find(i) != None)
        en = time.time()
        print(f"Time to search sample in given binary tree: {en - st}")


        print("Testing with balanced tree")
        st = time.time()
        self.rebalance()
        en = time.time()
        print(f"Time to rebalance binary tree: {en - st}")

        
        st = time.time()
        for i in selected:
            assert (self.find(i) != None)
        en = time.time()
        print(f"Time to search sample in given balanced binary tree: {en - st}")


z = LinkedBST()
z.demo_bst('words.txt')