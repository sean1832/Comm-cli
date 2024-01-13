import math

def convert_byte(byte, unit, percision: int=2):
    '''
    Convert byte to KB, MB, GB
    '''
    unit = unit.upper()

    if unit == 'KB':
        return round(byte / 1024, percision)
    elif unit == 'MB':
        return round(byte / (1024 * 1024), percision)
    elif unit == 'GB':
        return round(byte / (1024 * 1024 * 1024), percision)
    else:
        raise ValueError(f'Invalid unit {unit}')