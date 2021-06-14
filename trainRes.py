#用来将训练集的groundtruth.txt的所有文件集中到TrainResylt中

import os
count=0
for parent, dirnames, filenames in os.walk('trainval'):
    for dirname in dirnames:
        print(len(dirnames))
        for parent, dirnames, filenames in os.walk("trainval/"+dirname):
            for filename in filenames:
                if filename=="groundtruth.txt":
                    count=count+1
                    f = open(  "TrainResult/" + dirname + ".txt", 'w')
                    f1=open("trainval/"+dirname+"/"+filename)
                    f.write(f1.read())
                    f.close()
                    f1.close()
print(count)