import matplotlib.pyplot as plt
import numpy as np

class MinimapPlotter:
    """
    Class for creating and updating a minimap utilising player coordinates from Minecraft.
    """
    def __init__(self) -> None:
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_aspect('equal', adjustable='box')
    
    def update_minimap(self, first_coord: np.ndarray, chunk_range: int, direction: str) -> None:
        """
        Update player's position on the minimap
        """
        # Clear previous plot
        self.ax.cla()

        # Assing player coordinates and player chunk range
        self.x_pos, self.z_pos = first_coord[0], first_coord[2]
        self.chunk_range = chunk_range

        # Chunk coordinate
        self.x_chunk = self.x_pos//16
        self.z_chunk = self.z_pos//16

        # Upper and lower bounds for Z and X chunk
        minor_x_chunk = (self.x_chunk - self.chunk_range) * 16
        major_x_chunk = (self.x_chunk + self.chunk_range + 1) * 16

        minor_z_chunk = (self.z_chunk - self.chunk_range) * 16
        major_z_chunk = (self.z_chunk + self.chunk_range + 1) * 16

        # Major ticks as 16x16 chunk representation
        major_ticks_x = np.arange(minor_x_chunk, major_x_chunk, 16)
        major_ticks_z = np.arange(minor_z_chunk, major_z_chunk, 16)

        # Set the plot limits based on the updated data
        self.ax.set_xlim(minor_x_chunk, major_x_chunk)
        self.ax.set_ylim(minor_z_chunk, major_z_chunk)

        # Update major ticks
        self.ax.set_xticks(major_ticks_x)
        self.ax.set_yticks(major_ticks_z)
        self.ax.grid(which='major')

        # Update the scatter plot
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.scatter(self.x_pos, self.z_pos)

        arrow_length = 3  # Length of the arrow

        # Plot arrow
        # None direction is handled
        try:
            if direction.upper() == 'N':
                self.ax.annotate('', xy=(self.x_pos, self.z_pos - arrow_length), xytext=(self.x_pos, self.z_pos), arrowprops=dict(facecolor='cyan', arrowstyle='->'))
            elif direction.upper() == 'S':
                self.ax.annotate('', xy=(self.x_pos, self.z_pos + arrow_length), xytext=(self.x_pos, self.z_pos), arrowprops=dict(facecolor='cyan', arrowstyle='->'))
            elif direction.upper() == 'W':
                self.ax.annotate('', xy=(self.x_pos - arrow_length, self.z_pos), xytext=(self.x_pos, self.z_pos), arrowprops=dict(facecolor='cyan', arrowstyle='->'))
            elif direction.upper() == 'E':
                self.ax.annotate('', xy=(self.x_pos + arrow_length, self.z_pos), xytext=(self.x_pos, self.z_pos), arrowprops=dict(facecolor='cyan', arrowstyle='->'))
        except AttributeError:
            pass