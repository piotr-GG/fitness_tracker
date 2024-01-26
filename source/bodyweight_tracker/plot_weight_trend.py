import pandas as pd

import bokeh
from definitions import INPUT_PATH

input_file_path = INPUT_PATH.joinpath("weight_input.csv")
print(input_file_path)

df = pd.read_csv(input_file_path, parse_dates=[0], date_format="%d.%m.%y")