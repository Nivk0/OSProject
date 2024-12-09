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


Interactive Menu options thing

Create new index file
Open existing index file
Insert key/value
Search key
Load from CSV
Print all entries
Extract to CSV
Quit



Dec 2 3:04 PM
I implemented the basics of the project so far

But there are a lot of parts that are not implemented yet. 

Full B-Tree insertion logic in insert() method
Complete search functionality
Printing all index entries
CSV extraction

So far the code does this:
512-byte block size
Big-endian 8-byte integer storage
Header format with magic number
Minimal degree of 10 for the B-Tree

To complete the project, I need to add the more complex B-Tree operations like:

Split operations during insertions
Traversal for search
Handling node splits and tree growth



Dec 5 10:10 PM
I added alot to the btree implementation

Changes: 
Complete B-Tree insertion logic with node splitting
Finished the search functionality
Fully added the implementation of print_index()
Completed CSV extraction method
Added node caching 
Added code for recursive tree traversal

I can now create and open index correctly