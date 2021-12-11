#!/usr/bin/python

import math
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd

OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.legacy.TrackerCSRT_create(),
		"kcf": cv2.legacy.TrackerKCF_create(),
		"boosting": cv2.legacy.TrackerBoosting_create(),
		"mil": cv2.legacy.TrackerMIL_create(),
		"tld": cv2.legacy.TrackerTLD_create(),
		"medianflow": cv2.legacy.TrackerMedianFlow_create(),
		"mosse": cv2.legacy.TrackerMOSSE_create(),
}
colors = ["green", "blue", "red", "orange", "black", "pink", "purple", "yellow", "brown"]


def xywh_to_xyxy(bbox):
    return [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]


def intersection_over_union(bbox, gtbb):

    #convert from xywh to x0y0x1y1
    bbox = xywh_to_xyxy(bbox)
    gtbb = xywh_to_xyxy(gtbb)
 
    
    xA = max(bbox[0], gtbb[0])
    yA = max(bbox[1], gtbb[1])
    xB = min(bbox[2], gtbb[2])
    yB = min(bbox[3], gtbb[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)


    boxAArea = (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1)

    boxBArea = (gtbb[2] - gtbb[0] + 1) * (gtbb[3] - gtbb[1] + 1)
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def center_distance(bbox, gtbb):

    #convert from xywh to x0y0x1y1
    bbox = xywh_to_xyxy(bbox)
    gtbb = xywh_to_xyxy(gtbb)

    bboxcenterx = bbox[0] + bbox[2] / 2
    bboxcentery = bbox[1] + bbox[3] / 2
    gtbbcenterx = gtbb[0] + gtbb[2] / 2
    gtbbcentery = gtbb[1] + gtbb[3] / 2

    d1 = (bboxcenterx - gtbbcenterx) * (bboxcenterx - gtbbcenterx)
    d2 = (bboxcentery - gtbbcentery) * (bboxcentery - gtbbcentery) 
    
    dist = math.sqrt(d1 + d2)

    return dist

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

def compare(listgt, listbb):
    if len(listgt) != len(listbb):
        raise ValueError("mismatch between len of tracker and len of gt")
    center = []
    iou = []
    for i in range(len(listgt)):
        center.append(center_distance(listbb[i], listgt[i]))
        iou.append(intersection_over_union(listbb[i], listgt[i]))
    center = np.array(center)
    iou = np.array(iou)
    return center, iou
        

   

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", help="The number of the video")
    parser.add_argument("-at", "--alltrackers", action="store_true", help="Launch all trackers")
    parser.add_argument("-an", "--allnumbers", action="store_true", help="Launch all videos")
    parser.add_argument("-iou", "--IOU", action="store_true", help="intersection over union")
    parser.add_argument("-t", "--tracker", help="Tracker to use")
    parser.add_argument("-p", "--plot", help="Plots the results")
    
    opts = parser.parse_args()

    listtrackers = ["csrt", "kcf", "boosting", "mil", "tld", "medianflow", "mosse", "keeptrack", "dimp"]

    allcenter = []
    alliou = []
    if opts.allnumbers:
        for i in range(7):
            listgt = parseresults("groundtruth/" + str(i) + ".txt")
            if not opts.alltrackers:
                listtrackers = [opts.tracker]

            meancenter = []
            meaniou = []
            for opencvtracker in listtrackers:
                listtracker = parseresults("trackersresults/" + str(i) + "/" + opencvtracker + ".txt")

                center, iou = compare(listgt, listtracker)
                meancenter.append(np.mean(center))
                meaniou.append(np.mean(iou))
            allcenter.append(meancenter)
            alliou.append(meaniou)

    else:    
        listgt = parseresults("groundtruth/" + opts.number + ".txt")


        if not opts.alltrackers:
            listtrackers = [opts.tracker]

        meancenter = []
        meaniou = []
        for opencvtracker in listtrackers:
            listtracker = parseresults("trackersresults/" + opts.number + "/" + opencvtracker + ".txt")
            center, iou = compare(listgt, listtracker)
            meancenter.append(np.mean(center))
            meaniou.append(np.mean(iou))
            allcenter.append(meancenter)
            alliou.append(meaniou)

    print(len(listtrackers), len(allcenter), len(colors))

    if opts.IOU:
        Data = alliou
    else:
        Data = allcenter
    

    df3 = pd.DataFrame()
    for i in range(7):
        df = pd.DataFrame(Data[i]).T
        df3 = df3.append(df)

    df3.columns = listtrackers
    df3.insert(0, "video name", [0, 1, 2, 3, 4, 5,6], True)
    print(df3)
    print(df3.to_latex(index=False))
    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(111)
    for i in range(7):
        ax1.plot(listtrackers, Data[i], label = "video " + str(i), color = colors[i])
        ax1.scatter(listtrackers, Data[i], color = colors[i], marker='.', s=200)

    # x-axis label


    plt.xlabel('trackers')
    # frequency label
    plt.ylabel('ATA: average IOU')
    # plot title
    plt.title('ATA on the 9 trackers')
    # showing legend
    plt.legend()
    # function to show the plot
    if opts.IOU:
        plt.savefig('plots/iou.png')
    else:
        plt.savefig("plots/center.png")
    plt.show()
    
    






if __name__ == "__main__":
    main()