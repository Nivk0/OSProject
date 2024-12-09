import os
import struct
from btree import BTreeNode

class IndexManager:
    BLOCK_SIZE = 512
    MAGIC_NUMBER = b'4337PRJ3'
    MINIMAL_DEGREE = 10

    def __init__(self):
        self.file = None
        self.filename = None
        self.root_block_id = 0
        self.next_block_id = 1
        self._node_cache = {}

    def _read_node(self, block_id):
        """Read a node from the file."""
        if block_id in self._node_cache:
            return self._node_cache[block_id]

        with open(self.filename, 'rb') as f:
            f.seek(block_id * self.BLOCK_SIZE)
            node_data = f.read(self.BLOCK_SIZE)
            node = BTreeNode.deserialize(node_data)
            
            self._node_cache[block_id] = node
            return node

    def _write_node(self, node):
        """Write a node to the file."""
        with open(self.filename, 'r+b') as f:
            f.seek(node.block_id * self.BLOCK_SIZE)
            f.write(node.serialize().ljust(self.BLOCK_SIZE, b'\x00'))
        
        self._node_cache[node.block_id] = node

        if node.block_id >= self.next_block_id:
            self.next_block_id = node.block_id + 1
            self._update_header(next_block_id=self.next_block_id)

    def create_index_file(self, filename):
        if os.path.exists(filename):
            overwrite = input(f"File {filename} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                return False

        with open(filename, 'wb') as f:
            header = (
                self.MAGIC_NUMBER +
                struct.pack('>Q', 0) +  # Root block id
                struct.pack('>Q', 1)    # Next block id
            )
            header += b'\x00' * (self.BLOCK_SIZE - len(header))  # Pad to block size
            f.write(header)

        self.filename = filename
        self.root_block_id = 0
        self.next_block_id = 1
        self._node_cache = {}
        return True

    def open_index_file(self, filename):
        if not os.path.exists(filename):
            print(f"Error: File {filename} does not exist.")
            return False

        with open(filename, 'rb') as f:
            header = f.read(self.BLOCK_SIZE)
            
            if header[:8] != self.MAGIC_NUMBER:
                print("Error: Invalid file format.")
                return False

            self.root_block_id = struct.unpack('>Q', header[8:16])[0]
            self.next_block_id = struct.unpack('>Q', header[16:24])[0]

        self.filename = filename
        self._node_cache = {}
        return True

    def _find_node_with_key(self, key):
        if self.root_block_id == 0:
            return None, None

        current_node = self._read_node(self.root_block_id)
        while not current_node.is_leaf():
            for i, node_key in enumerate(current_node.keys):
                if key < node_key:
                    current_node = self._read_node(current_node.children[i])
                    break
            else:
                current_node = self._read_node(current_node.children[-1])

        return current_node, current_node.keys

    def insert(self, key, value):
        if self.root_block_id == 0:
            root = BTreeNode(block_id=self.next_block_id, parent_block_id=0)
            root.keys.append(key)
            root.values.append(value)
            
            self._write_node(root)
            self._update_header(root_block_id=root.block_id)
            return True

        existing_node, node_keys = self._find_node_with_key(key)
        if key in node_keys:
            print(f"Error: Key {key} exists already.")
            return False

        root = self._read_node(self.root_block_id)
        
        if root.is_full():
            new_root = BTreeNode(block_id=self.next_block_id, parent_block_id=0)
            new_root.children.append(self.root_block_id)
            
            root.parent_block_id = new_root.block_id
            y, z = new_root.split_child(0, root)
            
            self._write_node(new_root)
            self._write_node(y)
            self._write_node(z)
            
            self._update_header(root_block_id=new_root.block_id)
            root = new_root

        self._insert_non_full(root, key, value)
        return True

    def _insert_non_full(self, node, key, value):
        i = node.find_key_index(key)
        
        if node.is_leaf():
            node.keys.insert(i, key)
            node.values.insert(i, value)
            self._write_node(node)
            return

        child_block_id = node.children[i]
        child = self._read_node(child_block_id)

        if child.is_full():
            y, z = node.split_child(i, child)
            self._write_node(node)
            self._write_node(y)
            self._write_node(z)

            if key > node.keys[i]:
                child = self._read_node(node.children[i+1])
            else:
                child = self._read_node(node.children[i])

        self._insert_non_full(child, key, value)

    def search(self, key):
        """Search for a key in the B-tree."""
        if self.root_block_id == 0:
            print("Index is empty.")
            return None

        node, node_keys = self._find_node_with_key(key)
        
        if node and key in node_keys:
            index = node.keys.index(key)
            return (node.keys[index], node.values[index])
        
        print(f"Key {key} not found.")
        return None

    def _update_header(self, root_block_id=None, next_block_id=None):
        with open(self.filename, 'r+b') as f:
            if root_block_id is not None:
                f.seek(8)
                f.write(struct.pack('>Q', root_block_id))

            if next_block_id is not None:
                f.seek(16)
                f.write(struct.pack('>Q', next_block_id))

    def print_index(self):
        if self.root_block_id == 0:
            print("Index is empty.")
            return

        def traverse(block_id):
            node = self._read_node(block_id)
            
            if not node.is_leaf():
                for child_block_id in node.children[:-1]:
                    traverse(child_block_id)
            
            for key, value in zip(node.keys, node.values):
                print(f"Key: {key}, Value: {value}")
            
            if not node.is_leaf():
                traverse(node.children[-1])

        traverse(self.root_block_id)

    def load_from_csv(self, filename):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    key, value = map(int, line.strip().split(','))
                    self.insert(key, value)
            print(f"Successfully loaded data from {filename}")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def extract_to_csv(self, filename):
        if os.path.exists(filename):
            overwrite = input(f"File {filename} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                return

        try:
            with open(filename, 'w') as f:
                def traverse(block_id):
                    node = self._read_node(block_id)
                    
                    if not node.is_leaf():
                        for child_block_id in node.children[:-1]:
                            traverse(child_block_id)
                    
                    for key, value in zip(node.keys, node.values):
                        f.write(f"{key},{value}\n")
                    
                    if not node.is_leaf():
                        traverse(node.children[-1])

                traverse(self.root_block_id)
            
            print(f"Successfully extracted data to {filename}")
        except Exception as e:
            print(f"Error extracting to CSV: {e}")