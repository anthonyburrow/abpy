import logging
import os.path


default_log_dir = './log'


def setup_log(name=None, log_dir=None, log_to_file=False):
    print(log_to_file)
    # Setup root logger
    logging.basicConfig(format='')
    root = logging.getLogger('MY_LOG')
    root.setLevel(logging.INFO)
    root.propagate = False

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    root.addHandler(ch)

    if not log_to_file:
        return root

    # File handler
    if log_dir is None:
        log_dir = default_log_dir

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if name is None:
        name = 'my'

    filename = f'{log_dir}/{os.path.basename(name)}.log'
    fh = logging.FileHandler(filename, mode='w')
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    root.addHandler(fh)

    return root
