import pandas as pd

from ft_app.definitions import INPUT_PATH

input_file_path = INPUT_PATH.joinpath("weight_input.csv")
print(input_file_path)

df = pd.read_csv(input_file_path, parse_dates=[0], date_format="%d.%m.%Y")

# p = figure(width=400, height=400)
# p.line(df["Date"], df["Weight"], line_width=2)
# p.scatter(df["Date"], df["Weight"], size=8)
# show(p)
#
# print(df["Date"].dtype)

