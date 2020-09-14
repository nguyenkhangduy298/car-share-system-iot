import cv2
import time
image = cv2.imread("pysource_qrcode.png")
def readBarcode():
	cv2.namedWindow("preview")
	vc = cv2.VideoCapture(0)
	cache = ""
	results = None
	while rval:
	    cv2.imshow("preview", frame)
	    rval, frame = vc.read()
	    key = cv2.waitKey(20)
	    if key == ord('c'):
		    cv2.imwrite(image, frame)
			results = decodeFile(cache)
			print "Total count: " + str(len(results))
			for result in results:
				print "barcode format: " + formats[result[0]]
				print "barcode value: " + result[1] + "\n*************************"
	    elif key == 27:
	    	break

	cv2.destroyWindow("preview")

if __name__ == "__main__":
	print "OpenCV version: " + cv2.__version__
	readBarcode()