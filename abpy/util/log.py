import logging
import os.path


def setup_log(name=None, log_path='./log/'):
    if log_path[-1] == '/':
        log_path = log_path[:-1]

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    if name is None:
        name = 'my'

    # Root logger
    logging.basicConfig(format='')
    root = logging.getLogger('MY_LOG')
    root.setLevel(logging.INFO)
    root.propagate = False

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # File handler
    filename = f'{log_path}/{os.path.basename(name)}.log'
    fh = logging.FileHandler(filename, mode='w')
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    root.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    root.addHandler(ch)

    return root
