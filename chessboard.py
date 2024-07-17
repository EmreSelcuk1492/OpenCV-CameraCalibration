import cv2
import numpy as np

def createCheckerboard(boardWidth, boardHeight, rows, columns, squareSize):
    checkerboard = np.zeros((boardHeight, boardWidth), dtype=np.uint8)

    # Draw the squares
    for row in range(rows + 1):
        for col in range(columns + 1):
            if (row + col) % 2 == 0:
                cv2.rectangle(checkerboard, 
                              (col * squareSize, row * squareSize), 
                              ((col + 1) * squareSize, (row + 1) * squareSize), 
                              (255, 255, 255), -1)
    
    return checkerboard

boardWidth = 439  # Adjust based on your print area (300mm)
boardHeight = 300  # Adjust based on your print area (200mm)
rows = 8 
columns = 11
squareSize = 40 # 25mm

checkerboard = createCheckerboard(boardWidth, boardHeight, rows, columns, squareSize)
cv2.imwrite('chessboard.png', checkerboard)
cv2.imshow('chessboard', checkerboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
