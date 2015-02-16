import io
import picamera
import cv2
import numpy as np
import sys
import time
import picamera.array


def disp_multiple(im1 = None, im2 = None, im3 = None, im4 = None):
    height, width = im1.shape

    combined = np.zeros( (2*height, 2*width, 3), dtype=np.uint8)

    combined[0:height, 0:width, :] = cv2.cvtColor(im1, cv2.COLOR_GRAY2RGB)
    combined[height:, 0:width, :] = cv2.cvtColor(im2, cv2.COLOR_GRAY2RGB)
    combined[0:height, width:, :] = cv2.cvtColor(im3, cv2.COLOR_GRAY2RGB)
    combined[height:, width:, :] = cv2.cvtColor(im4, cv2.COLOR_GRAY2RGB)
#    cv2.SetImageROI(combined, 0*width, 0*height, width, height)
#    cv2.Copy(im1, combined)
#    cv2.ResetImageROI(combined)

    return combined

def label(image, text):
    return cv2.putText(image, text, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)    

def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    print in_min, in_max

    out = im - in_min
    out *= ( (out_min - out_max) / (in_min - in_max))
    out += in_min

#    out[out > out_max] = out_max
 #   out[out < out_min] = out_min

    return out

with picamera.PiCamera() as camera:
    x = 400
    camera.resolution = (int(1.33*x), x)
#    camera.framerate = 5
#    camera.awb_mode = 'off'
#    camera.awb_gains = (0.5, 0.5)
    time.sleep(1)

    
    with picamera.array.PiRGBArray(camera) as stream:
        while True:
            camera.capture(stream, format='bgr', use_video_port=True)
            image = stream.array

            b,g,r = cv2.split(image)
#            ndvi = cv2.divide( cv2.subtract(b, r)   , cv2.add(b, r)   )
            bottom = (r.astype(float) + b.astype(float))

            bottom[bottom == 0] = 0.01
            ndvi = (r.astype(float) - b) / bottom
            ndvi = contrast_stretch(ndvi)
            ndvi = ndvi.astype(np.uint8)
 
            label(b, 'Blue')
            label(g, 'Green')
            label(r, 'NIR')
            label(ndvi, 'NDVI')

            combined = disp_multiple(b, g, r, ndvi)

            cv2.imshow('image', combined)
            stream.truncate(0)
#            time.sleep(1)

            c = cv2.waitKey(7) % 0x100
            if c == 27:
                break

#time.sleep(100)        
cv2.destroyAllWindows()
