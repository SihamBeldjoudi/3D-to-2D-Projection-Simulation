import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""#Dataset**"""

data = pd.read_csv('data.csv')
data.head()

"""## **Constants**"""

f = 3  # Focal length of the camera
v = 3  # Speed or velocity of the camera (in arbitrary units)
R = 0.1  # Radius of the circular path along which the camera moves
times = np.linspace(0, 0.4, 10)  # Time intervals for the camera movement (not used directly here)

"""# **3D Points to 2D Projection: Circular Camera Path and Perspective Transformations**"""

# 3D Points: Read 3D coordinates from the 'data' DataFrame (assuming it's loaded previously)
points = np.array([data['X'], data['Y'], data['Z']]).T  # Convert to a NumPy array and transpose for easier use

# Create a figure for plotting with a specific size
fig = plt.figure(figsize=(20, 15))

# 3D Plot: Set up the first subplot for 3D visualization
fig1 = fig.add_subplot(121, projection='3d')
fig1.set_title('3D')  # Set the title of the 3D plot
fig1.set_xlabel('X')  # Label the X-axis
fig1.set_ylabel('Y')  # Label the Y-axis
fig1.set_zlabel('Z')  # Label the Z-axis

# Plot the 3D points in the 3D plot using blue color and 'p' marker shape
fig1.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue', marker='p', s=20)

# Convert 3D points to homogeneous coordinates by appending 1's to each point
points_3D_homogenes = np.hstack((points, np.ones((points.shape[0], 1))))  # Add a column of ones

# 2D Plot: Set up the second subplot for 2D visualization
fig2 = fig.add_subplot(122)
fig2.set_title('2D')  # Set the title of the 2D plot
fig2.set_xlabel('x')  # Label the x-axis of the 2D plot
fig2.set_ylabel('y')  # Label the y-axis of the 2D plot

# Define a set of colors for the different camera angles in the 2D plot
colors = plt.cm.viridis(np.linspace(0, 1, 10))

# Loop over camera positions by varying the angle theta from 0 to 2π
for idx, theta in enumerate(np.linspace(0, 2 * np.pi, 10)):  # 10 camera angles
    # Calculate the camera's position (Ax, Ay) on the circular path
    Ax = R * np.cos(theta)
    Ay = R * np.sin(theta)
    bx, by = Ax, Ay  # The translation offsets

    # Plot the camera position in the 3D plot (red 'p' markers)
    fig1.scatter(Ax, Ay, 0, color='red', marker='p', s=50, label=f'Pos{idx}')
    fig1.text(Ax, Ay, 0, 'Cam', c='r', fontsize=10)

    # Create the transformation matrices for the camera and the perspective
    Mai1 = np.array([[1, 0, 0, Ax], [0, 1, 0, Ay], [0, 0, 1, 0], [0, 0, 0, 1]])  # Camera transformation matrix (position)
    Mtl1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, -1 / v, 1]])  # Perspective matrix (based on velocity)

    # Multiply the transformation matrices to get the final combined matrix
    Mul1 = Mtl1 @ Mai1

    # Projection of 3D points to 2D using the transformation matrix
    points_2D_homogenes = []  # List to store the projected 2D points
    for point in points_3D_homogenes:
        z = point[2]  # Get the z-coordinate of the point
        if z != 0:  # If z is not zero, perform projection
            # Perspective projection matrix (taking focal length and camera position into account)
            Mpp1 = np.array([[-f / z, 0, -bx, 0], [0, -f / z, -by, 0], [0, 0, 1 / z, 0]])
            M1 = Mpp1 @ Mul1  # Apply the combined transformation matrix
            point_2D_homogene = M1 @ point  # Project the 3D point to 2D
            points_2D_homogenes.append(point_2D_homogene)
        else:
            points_2D_homogenes.append(np.zeros(4))  # If z = 0, set the point to (0,0,0)

    points_2D_homogenes = np.array(points_2D_homogenes)  # Convert the list of 2D points to an array

    # Convert homogeneous 2D points to standard 2D coordinates (by dividing by the z-coordinate)
    x_2D = points_2D_homogenes[:, 0] / points_2D_homogenes[:, 2]
    y_2D = points_2D_homogenes[:, 1] / points_2D_homogenes[:, 2]

    # Apply translation to the 2D points based on the camera position (bx, by)
    translation_matrix = np.array([[1, 0, bx], [0, 1, by], [0, 0, 1]])
    points_2D = np.vstack((x_2D, y_2D, np.ones_like(x_2D)))  # Stack the 2D points with ones for homogeneous coordinates
    points_2D_translated = translation_matrix @ points_2D  # Apply the translation

    # Extract the translated x and y coordinates
    x_2D_translated = points_2D_translated[0, :]
    y_2D_translated = points_2D_translated[1, :]

    # Plot the translated 2D points in the second plot with color coding for each camera angle
    fig2.scatter(x_2D_translated, y_2D_translated, color=colors[idx % len(colors)],
                 label=f'Angle= {np.degrees(theta):.1f}°, Ax={Ax:.2f}, Ay={Ay:.2f}',
                 marker='+', s=20)

# Set the x and y limits for the 2D plot
fig2.set_xlim(-1, 1)
fig2.set_ylim(-0.75, 1)

# Draw black lines for the x and y axes
fig2.axhline(0, color='black', linewidth=0.5)
fig2.axvline(0, color='black', linewidth=0.5)

# Set the aspect ratio of the 2D plot to be equal
fig2.set_aspect('equal', adjustable='box')

# Add a legend to the 2D plot
fig2.legend()

# Add gridlines to the 2D plot
fig2.grid()

# Adjust the layout to avoid overlap and show the plots
plt.tight_layout()

# Show the plots
plt.show()
