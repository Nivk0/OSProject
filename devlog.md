Dec 1 2:01PM
The project involves creating an interactive program that implements a B-Tree index manager.
Key functionalities include creating, opening, and managing index files using commands (create, open, insert, search, load, print, extract, quit).
The program must handle files with a fixed block size of 512 bytes and include both file and B-Tree headers.
The implementation should maintain only 3 B-Tree nodes in memory at a time.

Plan: My plan is to create files that imlement the following code

B-tree Implementation

Support minimal degree 10 (19 key/value pairs max per node)
512-byte block size
Big-endian byte storage
Root node tracking
Insertion logic
Search functionality


File Handler

Create index files
Write/read blocks
Manage header block
Handle big-endian conversions


Interactive Menu

Create new index file
Open existing index file
Insert key/value
Search key
Load from CSV
Print all entries
Extract to CSV
Quit