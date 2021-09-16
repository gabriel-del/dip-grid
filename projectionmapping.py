import math
import numpy as np, cv2

width = 640
height = 480

M2 = 0

# 4 reference points
referencePoints = np.float32([[width/4,height/4],[3*width/4,height/4],[3*width/4,3*height/4],[width/4,3*height/4]])

currentPoint = -1 # indicate wich point is selected
calibrating = True
fullScreen = False 

inputimage1 = cv2.imread("grid.png")
scale = cv2.imread("scale.png")
rows1, cols1 = inputimage1.shape[:2] # read dimensions of drid
pts1 = np.float32([[0,0],[cols1,0],[cols1,rows1],[0,rows1]]) # create points
image = np.zeros((height, width, 3), np.uint8) # create colorful image on screen

rgbcolor = (255,255,255)
selectedcolor = np.zeros((50, 50, 3), np.uint8) #cria uma imagem 50x50 para armazenar a cor selecionada

# color of dots
def pointColor(n):
	if n == 0:
		return (0,0,255)
	elif n == 1:
		return (0,255,255)
	elif n == 2:
		return (255,255,0)
	else:
		return (0,255,0)

# mouse events
def mouse(event, x, y, flags, param):
	if(not calibrating):
		return
	global currentPoint
	if event == cv2.EVENT_LBUTTONDOWN:
		if(x < 50 and y < 50):
			selectedcolor[:] = scale[y, x]

		cp = 0
        #discover which point you clicked (max distance: 4 pixels)
		for point in referencePoints:
			dist = math.sqrt((x-point[0])*(x-point[0])+(y-point[1])*(y-point[1]))
			if dist < 4:
				currentPoint = cp
				break
			else:
				cp = cp + 1

	if event == cv2.EVENT_LBUTTONUP: #when click is loose, tell it is -1
		pt = M2 @ (x, y, 1)
		pt = (pt/pt[2])
		if (pt[0] >= 0 and pt[0] < 490 and pt[1] >= 0 and pt[1] < 490):
			#print(int(pt[0]/70), " ", int(pt[1]/70))
			xx = int(pt[0]/70)
			yy = int(pt[1]/70)
			cv2.rectangle(inputimage1, (xx*70, yy*70), (xx*70+70, yy*70+70), (int(selectedcolor[0,0][0]),int(selectedcolor[0,0][1]),int(selectedcolor[0,0][2])), -1)

		currentPoint = -1
	if currentPoint != -1: #move the coordinates
		referencePoints[currentPoint] = [x,y]

# main window
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
#associate mouse events to main windo
cv2.setMouseCallback("test", mouse)

#it tels if select color is white
selectedcolor[:] = (255,255,255)

# main loop
while True:
	image[:] = (0,0,0) # clean image to black
	image[0:50,0:50] = scale
	image[0:50,width-50:width] = selectedcolor
	if calibrating: # change colored dots
		color = 0
		for point in referencePoints:
			cv2.circle(image, (int(point[0]), int(point[1])),5,pointColor(color), -1)
			color = color + 1

	M = cv2.getPerspectiveTransform(pts1,referencePoints) # calculate projection
	M2 = cv2.getPerspectiveTransform(referencePoints, pts1)
	cv2.warpPerspective(inputimage1, M, (width,height), image, borderMode=cv2.BORDER_TRANSPARENT) # project

	cv2.imshow("test", image)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("c"):
		calibrating = not calibrating

	if key == ord("f"):
		if fullScreen == False:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		else:
			cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
		fullScreen = not fullScreen

	if key == ord("q"):
		break

cv2.destroyAllWindows()
