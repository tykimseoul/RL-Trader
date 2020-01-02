import numpy as np

from functions import sigmoid


class State:
    def __init__(self, window_size, data, kospi, is_eval=False, target_size=0):
        self.target_size = target_size
        self.is_eval = is_eval
        self.data = {'intraday': data, 'kospi': kospi}
        self.window_size = window_size if not is_eval else int(target_size / len(self.data.keys())) + 1

    def get_instance(self, end_time):
        def get_block(data, end_time):
            d = end_time - self.window_size + 1
            block = data[d:end_time + 1] if d >= 0 else -d * [data[0]] + data[0:end_time + 1]  # pad with t0
            res = [sigmoid(block[i + 1] - block[i]) for i in range(self.window_size - 1)]
            return res

        stock_block = get_block(self.data['intraday'], end_time)
        kospi_block = get_block(self.data['kospi'], end_time)
        return np.array([np.append(stock_block, kospi_block)])

    def size(self):
        return len(self.get_instance(0)[0])
