import sys

import pandas as pd
import matplotlib.pyplot as plt


def read_csv_exception(csv_file_path):
    """Convert a csv file to a pandas dataframe with exception handling

        Args:
            df_file_path (str): file path to csv file

        Returns:
            df (DataFrame): pandas dataframe
    """
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except FileNotFoundError:
        print(f"Can't find:\n{str(csv_file_path)}")
        sys.exit()


def plot_intensities(df, area, intensities, power=False, MPP=None):

    n_colours = 12
    cmap = plt.cm.get_cmap('tab20')         # 20 distinct colours for plotting

    _, ax = plt.subplots()

    for key, value in intensities.items():

        # Colour of the line being plotted
        colour = cmap((key / 4) / n_colours)

        # Voltage values in Volts (V)
        voltage_vals = pd.to_numeric(df.iloc[:, key][1:])

        # Current values converted from amps (A) to milliamps (mA)
        current_vals = pd.to_numeric(df.iloc[:, (key + 1)][1:]) * 1000

        # Compute J
        current_density_vals = current_vals / area   # Units mAcm^-2

        # Plot the data
        if power:
            # P = IV
            power_vals = voltage_vals * current_vals
            plt.plot(voltage_vals, power_vals, color=colour, label=value)
        else:
            plt.plot(
                voltage_vals, current_density_vals, color=colour, label=value
                )

    # Centre the axes about the origin
    ax.spines['bottom'].set_position('zero')  # x-axis at y = 0
    ax.spines['left'].set_position('zero')    # y-axis at x = 0

    # Increments under the x-axis and to the left of y-axis
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Move labels to ends
    ax.xaxis.set_label_coords(0, 0)
    ax.yaxis.set_label_coords(0, 0)

    # Axes increments
    x_vals = [((i * 0.05) - 0.5) for i in range(35)]
    plt.xticks(x_vals, fontsize=16)

    # Labelling the plot
    plt.xlabel("Voltage / V", fontsize=32)

    if power:
        # Power-Voltage plot
        plt.title(
            "Power-Voltage plot of Light Intensities of Perovskite Solar Cell",
            fontsize=36
            )

        # Power values has smaller range than current density
        y_vals = [((i * 0.1) - 1) for i in range(37)]
        plt.yticks(y_vals, fontsize=20)
        plt.ylabel("Power / mW", fontsize=32)

    else:
        # JV plot
        plt.title(
            "JV curve of Light Intensities of a Perovskite Solar Cell",
            fontsize=36
            )

        # Current density has larger range than power values
        plt.yticks(range(-26, 50, 2), fontsize=20)
        plt.ylabel("Current Density / mAcm$^{-2}$", fontsize=32)

    # Plotting the Maximum Power Point (MPP)
    if MPP:
        for key, item in MPP.items():
            if power:
                MPP_y = item[1] * item[0]   # Power = Current * Voltage
                offset = 0.15
            else:
                MPP_y = item[1] / area  # Current density = Current / Area
                offset = 3

            # Plotting the MPP as X marker
            plt.plot(item[0], MPP_y, marker="x", markersize=25,
                     markeredgewidth=2)

            # Horizontal dashed line (from x=0 to x coordinate of MPP)
            ax.plot([0, item[0]], [MPP_y, MPP_y], linestyle="--",
                    linewidth=1)

            # Vertical dashed line (from y coordinate of MPP to y=0)
            ax.plot([item[0], item[0]], [0, MPP_y], linestyle="--",
                    linewidth=1)

            # Labelling the MPP
            plt.text(item[0], (MPP_y - offset), f"MPP {key}%", fontsize=30,
                     ha="left", va="bottom")

    # Legend for the plots of different intensities
    plt.legend(fontsize=24)

    # Maximise the window
    mng = plt.get_current_fig_manager()
    screen_width = mng.window.winfo_screenwidth()
    screen_height = mng.window.winfo_screenheight()
    mng.window.geometry(f"{screen_width}x{screen_height}+0+0")

    # plt.show()


# Pandas dataframe for the csv file data
data_df = read_csv_exception("CSV Data File.csv")

# Column indexes in the dataframe that represent each of the light intensities
intensity_all = {
                    0: "Light intensity 1%",
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

# Same as above but just for intensities 10%, 50% and 100%
intensity_10_50_100 = {
                        8: "Light intensity 10%",
                        28: "Light intensity 50%",
                        44: "Light intensity 100%",
                      }

# Maximum Power Point for 10%, 50% and 100%
max_power_points = {
            10: [0.85, -0.11],
            50: [0.89, -0.51],
            100: [0.89, -0.97]
}

# Area of solar cell in cm^2
solar_cell_area = 0.045

# JV Plots
plot_intensities(data_df, solar_cell_area, intensity_all)
plot_intensities(data_df, solar_cell_area, intensity_10_50_100,
                 MPP=max_power_points)

# Power-Voltage plot
plot_intensities(data_df, solar_cell_area, intensity_10_50_100, power=True,
                 MPP=max_power_points)

plt.show()
