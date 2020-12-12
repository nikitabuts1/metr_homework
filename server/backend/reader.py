import numpy as np
import os
from typing import List

class ReaderError(Exception):
    pass

def reader(path: str) -> np.array:
    if not os.path.exists(path):
        raise FileNotFoundError
    values: List[float] = []
    try:
        with open(path, 'r') as f:
            for line in f.readlines():
                values.extend(
                    [
                        float(
                            v.replace(',', '.')
                        ) for v in line.split()
                    ]
                )
    except:
        raise ReaderError
    return np.array(values)