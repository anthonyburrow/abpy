import logging
import os.path


def makelog(name=None, log_path='./log/'):
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    if name is None:
        name = '%smy' % log_path

    name += '.log'

    # Root logger
    logging.basicConfig(format='')
    root = logging.getLogger('MY_LOG')
    root.setLevel(logging.INFO)
    root.propagate = False

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # File handler
    name = '%s%s' % (log_path, os.path.basename(name))
    fh = logging.FileHandler(name, mode='w')
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    root.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    root.addHandler(ch)

    return root
