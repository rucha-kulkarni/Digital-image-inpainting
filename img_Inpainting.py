# Final Year Project_2020
# Project name - Digital Image Inpainting system
# Project is done using OpenCV

import numpy as np                                           #library used
import cv2 as cv

class Sketcher:                                              # used to draw with mouse to inpaint
#def __init__(self) is a constructor
    def __init__(self, windowname, dests, color_func):       # these are arguments
        self.prev_pt = None                                  # used to preserve previous points
        self.windowname = windowname
        self.dests = dests                                   # destorted output stored image
        self.color_func = color_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname,self.on_mouse)
# to show output
    def show(self):
        cv.imshow(self.windowname, self.dests[0])             # original image
        cv.imshow(self.windowname+":Mask", self.dests[1])     # mask
# to track mose events
    def on_mouse(self, event, x, y, flags, param):
        pt = (x,y)                                            # pts of mouse x, y will record in tuple
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_pt = pt                                 # pts will be saved in preserved_pts through pts
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_pt = None
 # to spread white pixels
        if self.prev_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.color_func()):
                cv.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()
          # collect every values to display in mask , zip is iterator of tuples ,collects pts & coordinates
          # show function will show image stored in dests
          # event is saved in event variable on left click
          # pixels represented in form of line by cv.line
# main function
def main():
    print('Usage: Python Inpaint')
    print('Keys:')
    print('t - inpaint using FMM')
    print('n - inpaint using NS technique')
    print('r - reset the inpaint mask')
    print('ESC - exit')
    # Read image in color mode
    path =r'example.png'
    img = cv.imread(path)
    cv.imshow('Example',img)

    if img is None:
        print('Fail to load image file: {}'.format(img))
        return
    img_mask = img.copy()                                              # copy is function to copy

    inpaintMask = np.zeros(img.shape[0:2], np.uint8)                   # datatype of image (uint8) - unsigned integer of 8 bit

    sketch = Sketcher('image', [img_mask, inpaintMask], lambda: ((255, 255, 255), 255))     # object of sketcher class
#logic
    while True:
        ch = cv.waitKey(0)

        if ch == 27:                 # ascii value of Esc
            break
        if ch == ord('t'):           # ord() - function in Python accepts a string of length 1
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=2, flags=cv.INPAINT_TELEA)    # cv.inpaint function
            cv.imshow('Inpaint output using FMM', res)    # Fast marching method
        if ch == ord('n'):
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintMask, inpaintRadius=2, flags=cv.INPAINT_NS)
            cv.imshow('Inpaint output using NS', res)     # Navier-Stokes based Inpainting
        if ch == ord('r'):
            img_mask[:] = img         # complete image
            inpaintMask[:] = 0        # restore mask image
            sketch.show()
        print('Completed')

if __name__ == "__main__":
    main()
    cv.destroyAllWindows()

