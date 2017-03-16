


TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hash_Table:

    def __init__(self,cells,defval):
        '''
        Construct a bnew hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.table = [None] * cells if cells>0 else [None]
        self.defval = defval
        self.cells = cells if cells>0 else 1
        self.num_element = 0
								

    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        index = hash(key) % self.cells
        for i in range(self.cells):
            search_idx = (i + index) % self.cells
            if self.table[search_idx] is not None:
                if self.table[search_idx][0] == key:
                    return self.table[search_idx][1]
            else:
                return self.defval

    def keys(self):
        return [key[0] for key in self.table if key is not None] 
		
    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        if self.num_element/float(self.cells) >= TOO_FULL:
            self._grow()
        index = hash(key) % self.cells
        for i in range(self.cells):
            search_idx = (i + index) % self.cells
            if self.table[search_idx] is not None:
                if self.table[search_idx][0] == key:
                    self.table[search_idx] = (key, val)
                    return
            else:
                self.table[search_idx] = (key, val)
                self.num_element +=1
                return

    def _grow(self):
        self.cells = self.cells * GROWTH_RATIO
        old_table = self.table
        self.table = [None] * self.cells
        self.num_element = 0
        for i in iter(old_table):
            if i is not None:
                self.update(i[0], i[1])
																



        