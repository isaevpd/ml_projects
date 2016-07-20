# Python 2.7

import numpy as np
import pandas as pd
from collections import OrderedDict

file_name = raw_input("Please enter the name of the file, don't forget the extension, e.g. 'prices.csv' without quotes:\n")
column = raw_input("Please enter the column name to use, e.g. 'PX_LAST' without quotes:\n")
interval = int(raw_input("Please enter an integer denoting interval, minimum is 1:\n"))
step = int(raw_input("Please enter an integer denoting step, minimum is 1:\n"))
start_date = raw_input("Please enter start date, e.g. '1997-12-31' without quotes:\n")
end_date = raw_input("Please enter end date, e.g. '2010-07-02' without quotes:\n")
to_write = raw_input("Write to output.csv y/n:\n")

# file_name = 'prices.csv'
# column = 'PX_LAST'
# interval = 3
# step = 1
# start_date = '1997-12-25'
# end_date = '1998-01-01'
# to_write = 'y'

# read file name provided, take the appropriate column
data = pd.read_csv(file_name).set_index('Date')[column]
data = data.loc[start_date if start_date else data.first_valid_index():end_date]


def get_start_date_interval(data, interval, step):
    return [(data.index[i]) for i in range(0, len(data) - interval + 1, step)]

def get_end_date_interval(data, interval, step):
    return [(data.index[i+interval-1]) for i in range(0, len(data) - interval + 1, step)]

# FIXME add exponential component
def get_exp_moving_average(data, interval, step):
    """
    input:
    list data, int interval, int step
    output:
    list of averages
    """
    return [round(np.mean(data[i:i+interval]), 3) for i in range(0, len(data) - interval + 1, step)]

def get_moving_average(data, interval, step):
    """
    input:
    list data, int interval, int step
    output:
    list of averages
    """
    return [round(np.mean(data[i:i+interval]), 3) for i in range(0, len(data) - interval + 1, step)]

def get_standard_deviation(data, interval, step):
    """
    input:
    list data, int interval, int step
    output:
    list of std values
    """
    return [round(np.std(data[i:i+interval]), 3) for i in range(0, len(data) - interval + 1, step)]

def get_max(data, interval, step):
    """
    input:
    list data, int interval, int step
    output:
    list of maximum values
    """
    return [np.max(data[i:i+interval]) for i in range(0, len(data) - interval + 1, step)]

def get_min(data, interval, step):
    """
    input:
    list data, int interval, int step
    output:
    list of minimum values
    """
    return [np.min(data[i:i+interval]) for i in range(0, len(data) - interval + 1, step)]

def get_increase(data, interval, step):
    """
    calculates the number of
    increase tendency
    in data
    input:
    list data, int interval, int step
    output:
    list of numbers the price increases
    """
    def helper(data):
        """
        returns the number of increases for values in data
        """
        return sum(1 for i in range(1, len(data)) if data[i] > data[i - 1])

    return [helper(data[i:i+interval]) for i in range(0, len(data) - interval + 1, step)]


def get_decrease(data, interval, step):
    """
    calculates the number of
    decrease tendency
    in data
    input:
    list data, int interval, int step
    output:
    list of numbers the price decreases
    """
    def helper(data):
        """
        returns the number of decreases for values in data
        """
        return sum(1 for i in range(1, len(data)) if data[i] < data[i - 1])

    return [helper(data[i:i+interval]) for i in range(0, len(data) - interval + 1, step)]

def get_equal(data, interval, step):
    """
    calculates the number of
    decrease tendency
    in data
    input:
    list data, int interval, int step
    output:
    list of numbers the price stays the same
    """
    def helper(data):
        """
        returns the number of equals for values in data
        """
        return sum(1 for i in range(1, len(data)) if data[i] == data[i - 1])

    return [helper(data[i:i+interval]) for i in range(0, len(data) - interval + 1, step)]


def write_result(output_file, to_write=False, data=data, interval=interval, step=step):
    with open(output_file, 'w') as f:
        feature_functions = OrderedDict([
            ('start', get_start_date_interval),
            ('end', get_end_date_interval),
            ('ema', get_exp_moving_average),
            ('ma', get_moving_average),
            ('sigma', get_standard_deviation),
            ('max', get_max),
            ('min', get_min),
            ('up', get_increase),
            ('down', get_decrease),
            ('flat', get_equal)
        ])

        result_data = pd.DataFrame({name: function(
            data, interval, step) for name, function in feature_functions.items()},
            columns=feature_functions.keys())
        
        if to_write:
            result_data.to_csv(output_file, index=False)
        else:
            print result_data


write_result('output.csv', {'y': True}.get(to_write, False))



