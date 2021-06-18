from numpy import savetxt


def write_data(data, filename: str, delimiter: str = '    ', heads=[],
               after_decimal: int = 3):
    '''Write structured array to file.'''
    header = []
    fmt = []

    for i, col in enumerate(data.dtype.names):
        try:
            _ = float(data[col][0])
            data_type = f'.{after_decimal}f'
            align = ''
        except ValueError:
            data_type = 's'
            align = '-'

        col_data = data[col].astype(str)
        max_char = len(max(col_data, key=len))

        if heads:
            _header = heads[i]
        else:
            _header = col
        max_char = max(max_char, len(_header))
        _header = f'%-{max_char}s' % _header
        header.append(_header)

        _fmt = f'%{align}{max_char}{data_type}'
        fmt.append(_fmt)

    header = delimiter.join(header)

    savetxt(filename, data, delimiter=delimiter, fmt=fmt, header=header,
            comments='')
