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

    def is_full(self):
        return len(self.keys) == self.MAX_KEYS

    def serialize(self):
        # Serialize node to bytes for file storage
        # Follow the block format specified in the project description
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
        # Deserialize bytes back into a node
        node = cls()
        node.block_id = struct.unpack('>Q', data[0:8])[0]
        node.parent_block_id = struct.unpack('>Q', data[8:16])[0]
        key_count = struct.unpack('>Q', data[16:24])[0]

        # Extract keys, values, and children
        node.keys = [struct.unpack('>Q', data[24+i*8:32+i*8])[0] for i in range(19)][:key_count]
        node.values = [struct.unpack('>Q', data[216+i*8:224+i*8])[0] for i in range(19)][:key_count]
        node.children = [struct.unpack('>Q', data[408+i*8:416+i*8])[0] for i in range(20)]

        # Remove trailing zeros
        node.keys = node.keys[:key_count]
        node.values = node.values[:key_count]
        node.children = [child for child in node.children if child != 0]

        return node