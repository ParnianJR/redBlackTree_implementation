class RedBlackTree:
    class Node:
        def __init__(self, key, left = None, right = None, parent = None):
            self._key = key
            self._parent = parent
            self._left = left
            self._right = right
            self._red = False
            self._extra_black = False
            
    def __init__(self):
        self._nil = self.Node(None)
        self._set_black(self._nil)
        self._root = self._nil
        self.size = 0
        
    def _set_red(self, p): p._red = True
    def _set_black(self, p): p._red = False
    def _is_red(self, p): return p._red        
    def set_extra_black(self, p): p._extra_black = True
    def remove_extra_black(self, p): p._extra_black = False

    def _left_rotate(self, x):
        y = x._right
        x._right = y._left  

        if y._left != self._nil:
            y._left._parent = x
            
        y._parent = x._parent  

        if x._parent == self._nil:
            self._root = y
        elif x == x._parent._left:
            x._parent._left = y
        else:
            x._parent._right = y

        y._left = x  
        x._parent = y
        
        
    def _right_rotate(self, y):
        x = y._left
        y._left = x._right
        
        if x._right != self._nil:
            x._right._parent = y
            
        x._parent = y._parent
        
        if y._parent == self._nil:
            self._root = x
        elif y == y._parent._left:
            y._parent._left = x
        else:
            y._parent._right = x
        
        x._right = y
        y._parent = x    
        
        
    def RB_insert(self, x):
        prep = self._nil
        p = self._root
        while  p != self._nil :
            prep = p
            
            if x < p._key:
                p = p._left
                
            elif x > p._key:
                p = p._right
                
            else:
                return
            
        new_node = self.Node(x, self._nil, self._nil, prep)
        self._set_red(new_node)
        self.size +=1
        
        if prep == self._nil:
            self._root = new_node
        elif x < prep._key:
            prep._left = new_node
        else:
            prep._right = new_node
            
        self._RB_insert_fixup(new_node)
        
    def _RB_insert_fixup(self, z):
        
        while z != self._root and self._is_red(z._parent):
            
            parent = z._parent
            grand = z._parent._parent
            
            if parent == grand._left:
            #z in left subtree of grandparent
                
                uncle = grand._right
                
                if self._is_red(uncle):
                    
                    self._set_black(parent)                 # Case 1
                    self._set_black(uncle)                  # Case 1
                    self._set_red(grand)                    # Case 1
                    z = grand                               # Case 1
                    
                else:
                    if z == parent._right:
                        z = parent                          # Case 2a
                        self._left_rotate(z)                # Case 2a
                    
                    # It's possible that z has been changed
                    self._set_black(z._parent)              # Case 2b
                    self._set_red(z._parent._parent)        # Case 2b
                    self._right_rotate(z._parent._parent)   # Case 2b
                    
            else:
                #z in right subtree of grandparent
                uncle = grand._left
                
                if self._is_red(uncle):
                    
                    self._set_black(parent)
                    self._set_black(uncle)
                    self._set_red(grand)
                    z = grand
                    
                else:
                    if z == parent._left:
                        z = parent
                        self._right_rotate(z)
                        
                    # It's possible that z has been changed
                    self._set_black(z._parent)           
                    self._set_red(z._parent._parent)
                    self._left_rotate(z._parent._parent)
                    
        self._root._red = False
        
        
    def _preorder(self, p):
        if p == self._nil:
            return
        print (p._key, end = ',')
        print ("R" if self._is_red(p) else "B", end = ' ')
        self._preorder(p._left)
        self._preorder(p._right)
        
    def preorder(self):
        self._preorder(self._root)
        print()

    def _find_min(self, r):
        if r._left is None:
            return r
        return self._find_min(r._left)
    def find_min(self):
        return self._find_min(self._root)._key
    
    def _find_successor(self, r):
        if r._right is not None:
            return self._find_min(r._right)
        y = r._parent
        while y is not None and r == y._right_child:
            r = y
            y = y._parent
        return y

    def recolor(self, x):
        x._red = True if x._red == False else False
    
    def _delete(self,r , x):
        if r is None:
            raise Exception('this element is not in the red_black tree')
        if x < r._key :
            return self._delete(r._left, x)
        elif x > r._key:
            return self._delete(r._right, x)
        elif x == r._key:
            return r
    
    def delete(self, num):
        z = self._delete(self._root, num)
        self.RB_Delete(z)
    
    def RB_Delete(self,z):
        if z._left == self._nil or z._right == self._nil:
            y = z
        else : y = self._find_successor(z)
        x = y._left if not y._left == self._nil else y._right
        x._parent = y._parent
        if y._parent == self._root:
            self._root = x
        else:
            if y == y._parent._left:
                y._parent._left = x
            else : y._parent._right = x
        if not y == z:
            z._key = y._key
        if not y._red:
            self.RB_Delete_fixup(x)
        return y

    def RB_Delete_fixup(self, x):
        while x._extra_black == True and not x == self._root:
            if x == x._parent._left : # x is left child
                w = x._parent._right
                if w._red == True: #case 1
                    b = x._parent
                    d = w
                    self.recolor(b)
                    self.recolor(d)
                    self._left_rotate(b)
                    w = x._parent._right
                elif w._red == False and w._left._red == False and w._right._red == False: #case 2
                    self._set_red(w)
                    x = x._parent
                    if self._is_red(x):
                        self._set_black(x)
                        self.remove_extra_black(x)
                elif w._red == False and w._left._red == True and w._right._red == False: #case 3
                    c = w._left
                    self._set_black(c)
                    self._set_red(w)
                    self._right_rotate(w)
                    w = x._parent._right
                elif w._red == False and w._right_red == True: #case 4
                     b = x._parent
                     c = w
                     e = w._right
                     self._left_rotate(b)
                     self.remove_extra_black(x)
                     self.recolor(b)
                     self.recolor(c)
                     self.recolor(e)
        else: # x is right child
            w = x._parent._left
            if x._red == True: # case 1
                b = x._parent
                d = w
                self.recolor(b)
                self.recolor(d)
                self._right_rotate(b)
                w = x._parent._left
            elif w._red == False and w._left._red == False and w._right._red == False: #case 2
                self._set_red(w)
                x = x._parent
                if self._is_red(x):
                    self._set_black(x)
                    self.remove_extra_black(x)
            elif w._red == False and w._right._red == True and w._left._red == False: #case 3
                c = w._right
                self._set_black(c)
                self._set_red(w)
                self._left_rotate(w)
                w = x._parent._left
            elif w._red == False and w._left_red == True: #case 4
                b = x._parent
                c = w
                e = w._left
                self._right_rotate(b)
                self.remove_extra_black(x)
                self.recolor(b)
                self.recolor(c)
                self.recolor(e)
t = RedBlackTree()
for i in range(1,7):
    t.RB_insert(i)
t.preorder()
t.delete(5)
t.preorder()