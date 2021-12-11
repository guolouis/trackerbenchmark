#!/usr/bin/python

import argparse
import cv2


OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.legacy.TrackerCSRT_create(),
		"kcf": cv2.legacy.TrackerKCF_create(),
		"boosting": cv2.legacy.TrackerBoosting_create(),
		"mil": cv2.legacy.TrackerMIL_create(),
		"tld": cv2.legacy.TrackerTLD_create(),
		"medianflow": cv2.legacy.TrackerMedianFlow_create(),
		"mosse": cv2.legacy.TrackerMOSSE_create(),
}

def parseresults(path):
    myfile = open(path, "r")
    L=[]
    for line in myfile:
        newline = line.replace(',' , ' ')
        newline = newline.split()
        for i in range(4):
            newline[i] = int(float(newline[i]))
        L.append(newline)
    myfile.close()
    return L

def apply_bb(video_path, listbb):

    capture = cv2.VideoCapture(video_path)
    success, img = capture.read()
    i = 0
    while True:
        success, img = capture.read()
        x0, y0 = listbb[i][0], listbb[i][1]
        x1, y1 = x0 + listbb[i][2], y0 + listbb[i][3]
        if success:
            i += 1
            cv2.rectangle(img, (x0, y0), (x1, y1), (255, 0, 0), 3, 1)
            cv2.waitKey(50) 
        else:
            break
        cv2.imshow("Tracking", img)

    # When everything done, release the video capture object
    capture.release()
    # Closes all the frames
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="Number of the video")
    parser.add_argument("-t", "--tracker", help="Tracker to use")
    parser.add_argument("-g", "--gt", action="store_true", help="Apply groundtruth")

    opts = parser.parse_args()
    
    if not opts.gt:
        listbb = parseresults("trackersresults/" + opts.number + "/" + opts.tracker + ".txt")
        print(listbb)
    else:
        listbb = parseresults("groundtruth/" + opts.number + ".txt")
    video_path = "video/" + opts.number + ".mp4"
    apply_bb(video_path, listbb)


    

if __name__ == "__main__":
    main()

