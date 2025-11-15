import sys

import pandas as pd
import matplotlib.pyplot as plt


def read_csv_exception(csv_file_path):
    """Convert a csv file to a pandas dataframe with exception handling

        Args:
            df_file_path (pathlib.PosixPath): file path to csv file

        Returns:
            df (DataFrame): pandas dataframe
    """
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except FileNotFoundError:
        print(f"Can't find:\n{str(csv_file_path)}")
        sys.exit()


# Pandas dataframe for the csv file data
df = read_csv_exception("CSV Data File.csv")

# Columns in the dataframe that represent the different light intensities
intensity_cols = {0: "Light intensity 1%",
                  4: "Light intensity 3%",
                  8: "Light intensity 10%",
                  12: "Light intensity 16%",
                  16: "Light intensity 25%",
                  20: "Light intensity 32%",
                  24: "Light intensity 40%",
                  28: "Light intensity 50%",
                  32: "Light intensity 63%",
                  36: "Light intensity 79%",
                  40: "Light intensity 93%",
                  44: "Light intensity 100%",
                  }

solar_cell_area = 0.045     # Units cm^2

n_colours = 12
cmap = plt.cm.get_cmap('tab20')  # 20 distinct colors for plotting

fig, ax = plt.subplots()

for key, value in intensity_cols.items():
    colour = cmap((key / 4) / n_colours)

    # Voltage values in Volts (V)
    voltage_vals = pd.to_numeric(df.iloc[:, key][1:])

    # Current values converted from amps (A) to milliamps (mA)
    current_vals = pd.to_numeric(df.iloc[:, (key + 1)][1:]) * 1000

    # Compute J
    current_density_vals = current_vals / solar_cell_area   # Units mA cm^-2
    plt.plot(voltage_vals, current_density_vals, color=colour, label=value)

# Center the x-axis and y-axis
ax.spines['bottom'].set_position('zero')  # x-axis at y = 0
ax.spines['left'].set_position('zero')    # y-axis at x = 0

# Ticks only on bottom and left
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Move labels to ends
ax.xaxis.set_label_coords(0, 0)
ax.yaxis.set_label_coords(0, 0)

# Labelling the plot
plt.xlabel("Voltage / V", fontsize=32)
plt.ylabel("Current Density / mAcm$^{-2}$", fontsize=32)
plt.title(
    "JV curve of Light Intensities of a Perovskite Solar Cell", fontsize=36
    )
x_vals = [((i*0.05) - 0.5) for i in range(35)]
plt.legend(fontsize=16)
plt.xticks(x_vals, fontsize=16)
plt.yticks(range(-20, 50, 2), fontsize=16)
plt.show()
