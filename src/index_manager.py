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

    def create_index_file(self, filename):
        """Create a new index file."""
        # Check if file exists and handle overwrite
        if os.path.exists(filename):
            overwrite = input(f"File {filename} already exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                return False

        # Create/truncate the file and write header
        with open(filename, 'wb') as f:
            # Write magic number, root block (0), and next block (1)
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
        return True

    def open_index_file(self, filename):
        """Open an existing index file."""
        if not os.path.exists(filename):
            print(f"Error: File {filename} does not exist.")
            return False

        with open(filename, 'rb') as f:
            header = f.read(self.BLOCK_SIZE)
            
            # Verify magic number
            if header[:8] != self.MAGIC_NUMBER:
                print("Error: Invalid index file format.")
                return False

            # Extract root and next block ids
            self.root_block_id = struct.unpack('>Q', header[8:16])[0]
            self.next_block_id = struct.unpack('>Q', header[16:24])[0]

        self.filename = filename
        return True

    def insert(self, key, value):
        """Insert a key-value pair into the B-tree."""
        # If tree is empty, create root node
        if self.root_block_id == 0:
            root = BTreeNode(block_id=self.next_block_id, parent_block_id=0)
            root.keys.append(key)
            root.values.append(value)
            
            self._write_node(root)
            self._update_header(root_block_id=root.block_id)
            return True

        # TODO: Implement full B-tree insertion logic
        raise NotImplementedError("Full B-tree insertion not yet implemented")

    def search(self, key):
        """Search for a key in the B-tree."""
        if self.root_block_id == 0:
            print("Index is empty.")
            return None

        # TODO: Implement full B-tree search logic
        raise NotImplementedError("B-tree search not yet implemented")

    def _write_node(self, node):
        """Write a node to the file."""
        with open(self.filename, 'r+b') as f:
            f.seek(node.block_id * self.BLOCK_SIZE)
            f.write(node.serialize())
        self.next_block_id += 1

    def _update_header(self, root_block_id=None, next_block_id=None):
        """Update file header."""
        with open(self.filename, 'r+b') as f:
            # Update root block id if provided
            if root_block_id is not None:
                f.seek(8)
                f.write(struct.pack('>Q', root_block_id))

            # Update next block id if provided
            if next_block_id is not None:
                f.seek(16)
                f.write(struct.pack('>Q', next_block_id))

    def print_index(self):
        """Print all key-value pairs in the index."""
        # TODO: Implement index traversal and printing
        raise NotImplementedError("Index printing not yet implemented")

    def load_from_csv(self, filename):
        """Load key-value pairs from a CSV file."""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    key, value = map(int, line.strip().split(','))
                    self.insert(key, value)
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def extract_to_csv(self, filename):
        """Extract all key-value pairs to a CSV file."""
        # TODO: Implement extraction of all pairs to a CSV
        raise NotImplementedError("CSV extraction not yet implemented")