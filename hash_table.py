

class Node:
    def __init__(self, entry, next=None):
        self.key, self.value = entry
        self.next = next

    def is_equal(self, node):
        # FIXME recursive does not work
        if not (self.key == node.key and self.value == node.value):
            return False
        if node.next is None and self.next is None:
            return True
        else:
            return self.next.is_equal(node.next)

    def __str__(self):
        return f"Node: key={self.key}, value={self.value}, \n      next={self.next}"


class HashTable:
    def __init__(self, capacity=32, load_factor=0.75):
        self._capacity = capacity
        self._load_factor = load_factor
        self._nb_entries = 0
        self._array = [None for _ in range(self._capacity)]  # TODO Supposed to be a static array

    def __str__(self):
        entries = []
        for node in self._array:
            if node is not None:
                while node is not None:
                    entries.append((node.key, node.value))  # TODO Should be a static array with self._nb_entries slots
                    node = node.next
        return "{" + ", ".join([f"{key.__str__()}: {value.__str__()}" for key, value in entries]) + "}"

    def __repr__(self):
        return self._array.__repr__()

    def add(self, entry):
        key, _ = entry
        key_hash = self._get_hash(key)
        self._add_to_linked_list(key_hash, entry)

    def remove(self, entry):
        key, _ = entry
        key_hash = self._get_hash(key)
        self._remove_node(key, key_hash)

    def _remove_node(self, key, key_hash):
        node = self._array[key_hash]
        prev_node = None
        while node.key != key and node is not None:
            prev_node = node
            node = node.next
        if node is None:
            raise Exception("Cannot remove entry because it is not in the hashtable.")
        if prev_node is None:  # Remove the first element of the linked list
            self._array[key_hash] = node.next
        else:
            prev_node.next = node.next
            del node

    def get(self, key, default=None):
        key_hash = self._get_hash(key)
        node = self._array[key_hash]
        while node is not None and node.key != key:
            node = node.next
        if node is None:
            return default
        return node.value

    def _get_hash(self, key):
        return self._hash(key) % self._capacity

    def _add_to_linked_list(self, key_hash, entry):  # TODO Rename should be agnostic of underlying data structure
        key, value = entry
        if self._array[key_hash] is None:
            self._array[key_hash] = Node(entry)
        else:
            # TODO first check if the key is not already in the linkedlist
            node = self._array[key_hash]
            while node.next is not None:
                if node.key == key and node.value != value:
                    node.value = value
                    break
            if node.next is None:  # No node with key was found --> Add a new node with key
                new_node = Node(entry)
                node.next = new_node
                self._nb_entries += 1

    @staticmethod
    def _hash(key):
        return hash(key)


if __name__ == '__main__':
    ht = HashTable()
    ht.add((1, 3))
    assert ht._array[1].key == 1
    assert ht._array[1].value == 3
    assert ht._array[1].next is None
    assert ht._array[1].is_equal(Node((1, 3)))
    ht.add(("hash table", "One data structure to rule them all."))
    ht.add((33, 3))  # Test add hash collision
    ht.remove((33, 3))
    assert ht.get(1) == 3
    ht.remove((1, 3))
    assert ht.get(1) is None
    assert ht.get(1, default=100) == 100
