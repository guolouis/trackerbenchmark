# Video Tracking with Single Object Tracking

### Architecture of the files

**launchvideo.ipynb** is for applying the bounding box to get some visualisation

**experiments.ipynb** is for getting the graphs and tables

In the **video** folder, videos are numbered from 0 to 9, total of 10 videos.

In the **img** folder, each sub folder are numbered from 0 to 9 and contain the images/frames of the associated video.

In the **groundtruth folder** each file is numbered from 0 to 9 and is associated with the videos and are the groundtruth.

In the **trackersresults** folder,  each sub folder are numbered from 0 to 9 and contain the results of the 10 trackers on that video.

## COMMANDS

To launch a video number + tracker to visualize the video
``` python visuaize.py -n 0 -t keeptrack ```

To launch the evaluation on a tracker
``` python evaluation.py -n 0 -t csrt ```

To compute the txt outputfile of all the trackers on one video
``` python POCvideo.py -v video/0.mp4 -a -s -b ```



