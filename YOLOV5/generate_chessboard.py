import cv2
import numpy as np

# Chessboard pattern size (number of inner corners)
rows = 9
cols = 6
square_size = 50  # Size of each square in pixels

# Create a blank white image
chessboard = np.ones((rows * square_size, cols * square_size), dtype=np.uint8) * 255

# Draw the chessboard squares
for i in range(rows):
    for j in range(cols):
        if (i + j) % 2 == 0:
            cv2.rectangle(
                chessboard,
                (j * square_size, i * square_size),
                ((j + 1) * square_size, (i + 1) * square_size),
                0,
                -1
            )

# Display the chessboard pattern
cv2.imshow('Chessboard Pattern', chessboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
