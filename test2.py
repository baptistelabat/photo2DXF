import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import ndimage
import os, fnmatch

filename = '20191223_103818.jpg'
ImColor = cv2.imread(filename,cv2.IMREAD_COLOR)
plt.figure()
cv2.line(ImColor, (0, 829), (500, 829), (255, 0, 0), 3, 1)
cv2.line(ImColor, (0, 2446), (500, 2446), (255, 0, 0), 3, 1)
	

		
plt.imshow(ImColor)
print((2446-829.)/0.8)
plt.show()
