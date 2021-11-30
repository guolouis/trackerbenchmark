#!/usr/bin/python

import cv2
import argparse

OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.legacy.TrackerCSRT_create(),
		"kcf": cv2.legacy.TrackerKCF_create(),
		"boosting": cv2.legacy.TrackerBoosting_create(),
		"mil": cv2.legacy.TrackerMIL_create(),
		"tld": cv2.legacy.TrackerTLD_create(),
		"medianflow": cv2.legacy.TrackerMedianFlow_create(),
		"mosse": cv2.legacy.TrackerMOSSE_create(),
}

def writeresult(path, listbb):
    textfile = open(path, "w")
    for bb in listbb:
        for coord in bb:
            textfile.write(str(coord) + " ")
        textfile.write("\n")
    textfile.close()

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


def drawBox(img, x, y, w, h):
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3, 1)

def runtracker(inputfile, trackername, bbox):
    currenttracker = OPENCV_OBJECT_TRACKERS[trackername]
    capture = cv2.VideoCapture(inputfile)

    success, img = capture.read()
    if not bbox:
        bbox = cv2.selectROI("Target", img, False)

    res = []
    currenttracker.init(img, bbox)

    while True:
        now = cv2.getTickCount()
        success, img = capture.read()
        if success:
            success, bbox = currenttracker.update(img)
            if success:
                x, y, w, h = int(float(bbox[0])), int(float(bbox[1])), int(float(bbox[2])), int(float(bbox[3]))
                drawBox(img, x, y, w, h)
                cv2.putText(img, "Target", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                res.append([x, y, x + w, y + h])
            else:
                cv2.putText(img, "Lost", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                res.append(res[-1])

            fps = cv2.getTickFrequency() / (cv2.getTickCount() - now)
            
            cv2.putText(img, str(int(fps)), (30,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, trackername, (30,60), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow(trackername, img)
            cv2.waitKey(50) 
        else:
            break

    # When everything done, release the video capture object
    capture.release()
    # Closes all the frames
    cv2.destroyAllWindows()
    return res


 



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video_path", help="Path to the video")
    parser.add_argument("-a", "--alltrackers", action="store_true", help="Launch all trackers")
    parser.add_argument("-t", "--tracker", help="Tracker to use")
    parser.add_argument("-b", "--boundingbox", action="store_true", help="Use the default bounding box from the 1st frame of groundtruth")
    parser.add_argument("-s", "--save", action="store_true", help="Save the result into a .txt file in trackersresults/")

    opts = parser.parse_args()
    
    listtrackers = ["csrt", "kcf", "boosting", "mil", "tld", "medianflow", "mosse"]
    
    listGroundtruth = None
    if opts.boundingbox:
        bb = "groundtruth/" + opts.video_path.split('.')[0][-1] + ".txt"
        listGroundtruth = parseresults(bb)[0]

    if not opts.alltrackers:
        listtrackers = [opts.tracker]
    
        
    for opencvtracker in listtrackers:
        runtracker(opts.video_path, opencvtracker, listGroundtruth)


    


if __name__ == "__main__":
    main()


    
  








