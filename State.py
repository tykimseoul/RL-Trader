import numpy as np
from functions import sigmoid


class State:
    def __init__(self, window_size, data):
        self.window_size = window_size
        self.intraday_data = data

    def get_instance(self, end_time):
        d = end_time - self.window_size + 1
        block = self.intraday_data[d:end_time + 1] if d >= 0 else -d * [self.intraday_data[0]] + self.intraday_data[0:end_time + 1]  # pad with t0
        res = [sigmoid(block[i + 1] - block[i]) for i in range(self.window_size - 1)]

        return np.array([res])
