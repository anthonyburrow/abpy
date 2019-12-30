import pickle


class StateManager:

    def __init__(self, manager_name, path='./'):
        """Create state manager."""
        self.filename = f'{path}{manager_name}.p'

        self._state = {}
        self._setup()

    def _setup(self):

        try:
            self._state = pickle.load(open(self.filename, 'rb'))
        except (FileNotFoundError, EOFError):
            # Create 'blank' file with only {}
            self._save_state()

    def _save_state(self):
        """Save the current state."""
        pickle.dump(self._state, open(self.filename, 'wb'))

    def new(self, name: str):
        self._state[name] = {'data': None, 'complete': False}

    def remove(self, name: str):
        self._state.pop(name, None)

    def save(self, name: str, data):
        self._state[name]['data'] = data
        self._state[name]['complete'] = True
        self._save_state()

    def get(self, name: str):
        return self._state[name]['data']

    def is_complete(self, name: str):
        return self._state[name]['complete']

    def get_complete(self):
        for name in self._state:
            if self._state[name]['complete']:
                yield name

    def get_incomplete(self):
        for name in self._state:
            if not self._state[name]['complete']:
                yield name

    def reset(self, name: str):
        self._state[name]['complete'] = False

    def reset_all(self):
        for name in self._state:
            self.reset(name)
        self._save_state()
