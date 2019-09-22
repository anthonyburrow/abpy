import numpy as np


class Simulation:
    """Parametrized modelling"""

    def __init__(self, p0):
        try:
            self.init_cond = tuple(p0)
        except TypeError:
            self.init_cond = (p0)

        self.dep_var = []
        self.dep_var.append(self.init_cond)

    def run(self, func, t_range, n_frames, return_method='full'):
        # Checks
        assert isinstance(n_frames, int), "'n_frames' must be integer value."
        assert n_frames > 2, "n_frames' must be greater than or equal to 2."

        return_methods = ('full', 'generate')
        assert return_method in return_methods, \
            "'return_method' must be in: %s" % str(return_methods)
        self.return_method = return_method

        # Setup times and dt
        self.t_arr = np.linspace(*t_range, n_frames, endpoint=True)
        self.dt = self.t_arr[1] - self.t_arr[0]

        # Solve equation and return
        if self.return_method == 'generate':
            return self._run_gen(func, n_frames)
        elif self.return_method == 'full':
            return self._run_full(func, n_frames)

    def _run_gen(self, func, n_frames):
        f_prev = None
        for i in range(n_frames):
            if i == 0:
                f = self.dep_var[0]
            else:
                f = func(*f_prev, dt=self.dt)
            yield (self.t_arr[i], *f)
            f_prev = f

    def _run_full(self, func, n_frames):
        f_prev = None
        for i in range(n_frames):
            if i == 0:
                f = self.dep_var[0]
            else:
                f = func(*f_prev, dt=self.dt)
                self.dep_var.append(f)
            f_prev = f

        return [(t, *x) for t, x in zip(self.t_arr, self.dep_var)]
