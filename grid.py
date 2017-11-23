from collections.abc import MutableMapping


class GridError(Exception):
    pass


class Grid(MutableMapping):
    """ A dictionary with key checking based on a width and height """

    def __init__(self, height=19, width=19, initial_state=None):
        if width < 1 or height < 1:
            raise ValueError("Grid must have strictly positive width and height")
        self.width = int(width)
        self.height = int(height)
        if initial_state is not None:
            self._storage = initial_state
        else:
            self._storage = dict()

    def __repr__(self):
        class_name = type(self).__name__
        module = 'grid'
        return '%s.%s(height=%r, width=%r, state=%s)' % (module, class_name,
                                                         self.height, self.width, repr(self._storage))

    def __getitem__(self, key):
        return self._storage[key] if key in self._storage else None

    def __delitem__(self, key):
        del self._storage[key]

    def __setitem__(self, key, value):
        self._storage[key] = value

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __str__(self):
        return str(self._storage)

    def __contains__(self, key):
        return key in self._storage

    def __eq__(self, other):
        return (self.width == other.width
                and self.height == other.height
                and self._storage == other._storage)

