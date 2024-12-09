import os
import struct

class BTreeNode:
    def __init__(self, block_id=0, parent_block_id=0):
        self.block_id = block_id
        self.parent_block_id = parent_block_id
        self.keys = []
        self.values = []
        self.children = []
        self.MAX_KEYS = 19
        self.MINIMAL_DEGREE = 10

    def is_leaf(self):
        return len(self.children) == 0

    def is_full(self):
        return len(self.keys) == self.MAX_KEYS

    def find_key_index(self, key):
        for i, existing_key in enumerate(self.keys):
            if key < existing_key:
                return i
            if key == existing_key:
                return -1  # Key already exists
        return len(self.keys)

    def split_child(self, i, y):
        z = BTreeNode(block_id=y.block_id, parent_block_id=self.block_id)
        
        z.keys = y.keys[self.MINIMAL_DEGREE:]
        z.values = y.values[self.MINIMAL_DEGREE:]
        y.keys = y.keys[:self.MINIMAL_DEGREE-1]
        y.values = y.values[:self.MINIMAL_DEGREE-1]

        if not y.is_leaf():
            z.children = y.children[self.MINIMAL_DEGREE:]
            y.children = y.children[:self.MINIMAL_DEGREE]

        median_key = y.keys.pop()
        median_value = y.values.pop()
        
        self.keys.insert(i, median_key)
        self.values.insert(i, median_value)
        self.children.insert(i+1, z.block_id)

        return y, z

    def serialize(self):
        keys_bytes = b''.join(struct.pack('>Q', key) for key in self.keys + [0] * (19 - len(self.keys)))
        values_bytes = b''.join(struct.pack('>Q', value) for value in self.values + [0] * (19 - len(self.values)))
        children_bytes = b''.join(struct.pack('>Q', child) for child in self.children + [0] * (20 - len(self.children)))

        return (
            struct.pack('>Q', self.block_id) +  # Block ID
            struct.pack('>Q', self.parent_block_id) +  # Parent block ID
            struct.pack('>Q', len(self.keys)) +  # Number of keys
            keys_bytes +  # Keys
            values_bytes +  # Values
            children_bytes  # Child pointers
        )

    @classmethod
    def deserialize(cls, data):
        node = cls()
        node.block_id = struct.unpack('>Q', data[0:8])[0]
        node.parent_block_id = struct.unpack('>Q', data[8:16])[0]
        key_count = struct.unpack('>Q', data[16:24])[0]

        node.keys = [struct.unpack('>Q', data[24+i*8:32+i*8])[0] for i in range(19)][:key_count]
        node.values = [struct.unpack('>Q', data[216+i*8:224+i*8])[0] for i in range(19)][:key_count]
        node.children = [struct.unpack('>Q', data[408+i*8:416+i*8])[0] for i in range(20)]

        node.keys = node.keys[:key_count]
        node.values = node.values[:key_count]
        node.children = [child for child in node.children if child != 0]

        return node