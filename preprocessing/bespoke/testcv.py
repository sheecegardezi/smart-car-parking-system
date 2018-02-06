import cv2
import numpy as np


src='/Users/sheeced/Desktop/csproj17s2/artefacts/preprocessing/currentframe.jpg'
src=cv2.imread(src)
dst = cv2.resize(src, (700, 500), interpolation = cv2.INTER_CUBIC)

# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',dst)
    ch = cv2.waitKey()
    print(ch)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()

#windows
#enter_ch=13
#esc_ch=27
#space_ch=32
#n_ch=110
#d_ch=100