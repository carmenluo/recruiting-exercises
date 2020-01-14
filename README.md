# recruiting-exercises
#### Thougts:
1. Separate order and inventory into different class, easy to manipulate the whole object
2. Whole calculation is done in InventoryAllocator class, so if we want to change/add some logic in the future, we don't need to change other objects
3. Using pytest for unit testing

#### How to run
1. cd into inventory-allocator/src
2. run python3 inventoryallocator.py -o "{apple: 10}" -s "[{name: owd, inventory: { apple: 0 } }, { name: dm, inventory: { apple: 0 }}]" or python3 inventoryallocator.py -h for arguments info
3. install pytest to run test file
4. pytest -v 