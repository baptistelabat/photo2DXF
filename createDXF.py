import ezdxf
import os
import fnmatch
import numpy as np

scale = 1./2.02125*490./498.

dirList = os.listdir('C:\\Users\\baptiste.labat\\Documents\\perso\\Guillaume')
dirList = fnmatch.filter(dirList, '*.in.csv')
for filename in dirList:
	if os.path.exists(filename):
		data = np.genfromtxt(filename)*scale
		drawing = ezdxf.new(dxfversion='AC1024')
		modelspace = drawing.modelspace()
		points = []
		for dat in data:
			points.append((dat[1], dat[2])) #[(0, 0), (3, 0), (6, 3), (6, 6)]
		print(points)
		modelspace.add_lwpolyline(points)
		drawing.saveas(filename[:-11]+'.dxf')