# import the opencv library
import os
import cv2
import time
import numpy as np
import ctypes
import multiprocessing as mp
import math

import numpy as np
import itertools as it
import scipy.spatial.distance
import pyautogui

color_string = [
	'\x1b[30m', #Black
	'\x1b[34m', #Red
	'\x1b[32m', #Green
	'\x1b[36m', #Yellow
	'\x1b[31m', #Blue
	'\x1b[35m', #Magenta
	'\x1b[33m', #Cyan
	'\x1b[37m'  #White
	]


palette  = np.array([
	[0, 0, 0],#Black
	[255, 0, 0],#Red
	[0, 255, 0],#Green	
 	[255, 255, 0],#Yellow
	[0, 0, 255],#Blue
	[255, 0, 255],#Magenta
	[0, 255, 255],#Cyan
	[255, 255, 255]#White
])

valueRange = np.arange(0,256)
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^\`\\'. "
szChars = len(chars)
vid = cv2.VideoCapture("bonobono.mp4")
os.system("clear")
count = 0
while(True):
	ret, frame = vid.read()
	frame = cv2.resize(frame, (128, 128))
	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayShape = grayFrame.shape
	colorShape = frame.shape
	color_shared_array = mp.Array(ctypes.c_uint16, colorShape[0] * colorShape[1] * colorShape[2], lock=False)
	gray_shared_array = mp.Array(ctypes.c_uint16, grayShape[0] * grayShape[1], lock=False)
	colorBuffer = np.frombuffer(color_shared_array, dtype=np.uint16)
	grayBuffer = np.frombuffer(gray_shared_array, dtype=np.uint16)
	colorBuffer = colorBuffer.reshape(colorShape)
	grayBuffer = grayBuffer.reshape(grayShape)
	os.system("cls")
	if ret:
		count += 1
		grayBuffer[:] = grayFrame
		colorBuffer[:] = frame
		for i, row in enumerate(grayBuffer):
			for j, col in enumerate(row):
				val = math.ceil((szChars - 1) * col / 255)
				bgColor = color_string[scipy.spatial.distance.cdist([colorBuffer[i][j]], palette).argmin(1)[0]]
				print (bgColor + chars[val], end="")
			print()
		# time.sleep(0.2)

		
		# 캡쳐할 영상 위치를 region에 적어주세요..
		pic = pyautogui.screenshot(region=(254, 23, 1788, 1025))
		img_frame = np.array(pic)
		img_frame  = cv2.cvtColor(img_frame, cv2.COLOR_RGB2BGR)

		# 이미지를 캡쳐합니다
		cv2.imwrite(f"./images/cap{count:04d}.jpg", img_frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print ('\x1b[30m')
vid.release()
cv2.destroyAllWindows()

# 주의 사항
# 4K 해상도 명령창 전체모드
# 터미널 속성 들어가서
# 글꼴:래스터 글꼴 16x8
# 레이아웃: 화면버퍼크기 1271,278
# 레이아웃: 창크기 158,170
# 으로 맞춰주세요
#이미지를 다 캡쳐한 후 동영상 편집프로그램에서
# 음성을 입혀 렌더링해주면 끝!



