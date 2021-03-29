import pickle


class StateManager:

    def __init__(self, name: str, path: str='./'):
        """Create state manager.

        Args:
            name (str): Name of manager and state file.
            path (str): Path to place file.

        """
        self.filename = f'{path}{name}.p'

        self._state = {}
        try:
            self._state = pickle.load(open(self.filename, 'rb'))
        except (FileNotFoundError, EOFError):
            # Create 'blank' file with only { }
            self.save()

    def new(self, name: str):
        """Add new process to state to be completed.

        Args:
            name (str): Name of process.

        """
        self._state[name] = {'data': None, 'complete': False}

    def remove(self, name: str):
        """Remove process from state.

        Args:
            name (str): Name of process.

        """
        self._state.pop(name, None)

    def complete(self, name: str, data):
        """Add in completed process.

        Args:
            name (str): Name of process.
            data: Data (of any type) output from process.

        """
        self._state[name] = {'data': data, 'complete': True}

    def get(self, name: str):
        """Get data associated with process.

        Args:
            name (str): Name of process.

        Returns:
            data: Data output from process.

        """
        try:
            data = self._state[name]['data']
            return data
        except KeyError:
            return

    def is_process(self, name: str):
        """Check if process is in state.

        Args:
            name (str): Name of process.

        Returns:
            is_proc (bool): True if is process.

        """
        is_proc = name in self._state
        return is_proc

    def is_complete(self, name: str):
        """Check if process is complete.

        Args:
            name (str): Name of process.

        Returns:
            is_comp (bool): True if complete.

        """
        is_comp = self._state[name]['complete']
        return is_comp

    def get_complete(self):
        """Yield processes that are complete."""
        for name in self._state:
            if self._state[name]['complete']:
                yield name

    def get_incomplete(self):
        """Yield processes that are incomplete."""
        for name in self._state:
            if not self._state[name]['complete']:
                yield name

    def save(self):
        """Save the current state."""
        pickle.dump(self._state, open(self.filename, 'wb'))

    def reset(self, name: str):
        """Set process as incomplete.

        Args:
            name (str): Name of process.

        """
        self._state[name]['complete'] = False

    def reset_all(self):
        """Set every process in state as incomplete."""
        for name in self._state:
            self.reset(name)

    @property
    def count(self):
        """Get number of processes in state."""
        num = len(self._state)
        return num
