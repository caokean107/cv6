import cv2

import os
def point8tobbox(array):
    x = int(array[0])
    y = int(array[1])
    z = int(array[2] - array[0])+1
    w=int(array[5]-array[3])+1
    return x,y,z,w
def bboxtopoint8(bbox):
    x1=float(bbox[0])
    x2=float(bbox[0])+float(bbox[2])
    y1=float(bbox[1])
    y2=float(bbox[1])+float(bbox[3])
    return x1,y1,x2,y1,x2,y2,x1,y2
def point8tobbox1(array):
    x = int((array[2]+array[0])/2)
    y = int((array[1]+array[5])/2)
    z = int(array[2] - array[0])+1
    w=int(array[5]-array[3])+1
    return x,y,z,w
def bboxtopoint81(bbox):
    x1=float(bbox[0])-float(bbox[2])/2
    x2=float(bbox[0])+float(bbox[2])/2
    y1=float(bbox[1])-float(bbox[3])/2
    y2=float(bbox[1])+float(bbox[3])/2
    return x1,y1,x2,y1,x2,y2,x1,y2

def Txtfile(Dir,g,dirname):
    f = open(Dir+"/" + dirname + ".txt",'w')
    for line in g:
        for j in range(len(line)):
            if j!=len(line)-1:
                f.write(str(line[j])+",")
            else:
                f.write(str(line[j]) + "\n")
def Singletargettracking(Dir,dirname):

    #tracker = cv2.TrackerMIL_create()
    #tracker = cv2.TrackerKCF_create()
    tracker = cv2.TrackerCSRT_create()

    groundtruth=[]
    # Read first frame.
    frame =cv2.imread(Dir+"/"+dirname+"/00000001.jpg")
    f=open(Dir+"/"+dirname+"/groundtruth.txt")
    line=[float(i) for i in f.readline().split(',')]
    f.close()
    print(line)
    groundtruth.append(line)
    # Define an initial bounding box
    if dirname=="uwhgtyrn":
        return groundtruth
    x,y,z,w=point8tobbox(line)
    bbox = (x, y, z, w)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    for parent, dirnames, filenames in os.walk(Dir+"/" + dirname):
        for i in range(2,len(filenames)):
            # Read a new frame
            s=str(i)
            s=(8-len(s))*'0'+s
            frame = cv2.imread(Dir+"/" + dirname +"/"+s+".jpg")
            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok, bbox = tracker.update(frame)
            temp=[i for i in bboxtopoint8(bbox)]
            groundtruth.append(temp)
            # print(bbox)
            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                # print(p1)
                # print(p2)
            else:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                            2)

            # Display tracker type on frame
            cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display result
            cv2.imshow("Tracking", frame)

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
    return groundtruth
if __name__ == '__main__':
    Dir='test_public'
    for parent, dirnames, filenames in os.walk(Dir):
        for dirname in dirnames:
            print(dirname)
            g=Singletargettracking(Dir,dirname)
            Txtfile("181250004曹克安",g,dirname)
