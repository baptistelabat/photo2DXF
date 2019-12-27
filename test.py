import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import ndimage
import os, fnmatch
import csv

dirList = os.listdir('C:\\Users\\baptiste.labat\\Documents\\perso\\Guillaume')
dirList = fnmatch.filter(dirList, '*.jpg')
for filename in dirList[5:6]:
	#print(filename)
	img = cv2.imread(filename,cv2.cv2.IMREAD_GRAYSCALE)
	ImColor = cv2.imread(filename,cv2.IMREAD_COLOR)
	ImCopy = ImColor.copy()
	for i in range(2):
		ret,thresh = cv2.threshold(img,40,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
		contours,hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE )#CHAIN_APPROX_NONE or CHAIN_APPROX_SIMPLE
		plt.figure()
		contours.sort(key=lambda x:cv2.arcLength(x, True))
		contours = contours[-2:]
		#for contour in contours:
		#	print(cv2.arcLength(contour, True))
		for contour in contours:
			cv2.drawContours(ImColor, contour, -1, (0, 0, 255), 2)
		contour = contours[1]
		_, _, h, w = cv2.boundingRect(contour)
		epsilon = min(h, w) * 0.003
		vertices = cv2.approxPolyDP(contour, epsilon, True)

		rect = cv2.minAreaRect(contour)
		box = cv2.boxPoints(rect)
		box = np.int0(box)

		# get width and height of the detected rectangle
		width = int(rect[1][0])
		height = int(rect[1][1])

		src_pts = box.astype("float32")
		# corrdinate of the points in box points after the rectangle has been
		# straightened
		dst_pts = np.array([[0, height-1],
							[0, 0],
							[width-1, 0],
							[width-1, height-1]], dtype="float32")

		# the perspective transformation matrix
		M = cv2.getPerspectiveTransform(src_pts, dst_pts)


		cv2.drawContours(ImColor,[box],0,(0,255,255),2)
		# directly warp the rotated rectangle to get the straightened rectangle
		# font 
		font = cv2.FONT_HERSHEY_SIMPLEX 
		  
		# org 
		org = (50, 50) 
		  
		# fontScale 
		fontScale = 1
		   
		# Blue color in BGR 
		color = (255, 0, 0) 
		  
		# Line thickness of 2 px 
		thickness = 2
		for i_v in range(0,len(vertices),5):
			#print((vertices[i_v][0][0],vertices[i_v][0][1]))
			image = cv2.putText(ImColor, str(i_v), (vertices[i_v][0][0],vertices[i_v][0][1]), font,  
                   fontScale, color, thickness, cv2.LINE_AA)
	
		with open(filename +'.csv', 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for i_v in range(0,len(vertices)):
				spamwriter.writerow([str(i_v), vertices[i_v][0][0],vertices[i_v][0][1]])
		if os.path.exists(filename +'.in.csv'):
			data = np.genfromtxt(filename +'.in.csv')
			data = np.expand_dims(data[:,1:3], axis=1)
			# with open(filename +'.in.csv', newline='') as csvfile:
				# spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				# i_r = 0
				# new_vertices = []
				# for row in spamreader:
					# print(row)
					# i_r = i_r+1
					# new_vertices.append([int(row[1]), int(row[2])])
			# print(new_vertices)
			cv2.drawContours(ImColor, [data.astype(int)], -1, (0, 255, 0), 2)
		cv2.drawContours(ImColor, vertices, -1, (255, 0, 0), 2)
		
		plt.imshow(ImColor)
		ImColor = cv2.warpPerspective(ImCopy, M, (width, height))
		img     = cv2.warpPerspective(img, M, (width, height))
		if rect[2]>45:
			ImColor = np.rot90(ImColor,3).copy()
			img = np.rot90(img,3).copy()
		if rect[2]<-45:
			ImColor = np.rot90(ImColor,1).copy()
			img = np.rot90(img,1).copy()
		

plt.show()
