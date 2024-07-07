ra_hr = 9
ra_min = 55
ra_sec = 42.217

dec_deg = 69
dec_min = 40
dec_sec = 26.56

ra = ra_hr + ra_min / 60. + ra_sec / 3600.
ra *= 15.
dec = dec_deg + dec_min / 60. + dec_sec / 3600.

print(f'RA = {ra}')
print(f'DEC = {dec}')
