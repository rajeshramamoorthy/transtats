import cv2
import numpy as np
import collections

img = cv2.imread(r'\\172.16.0.6\cat\Charts\PNG Image\exes\withgray\11605829_0001.png', cv2.IMREAD_GRAYSCALE)
rows = img.shape
a = np.array(img)
demo = (max(a.sum(axis=1))*0.99) > a.sum(axis=1)
# counter = collections.Counter(demo)
# print(counter.most_common(3))
d=0
c = []
for i in range(len(a)):
    if demo[i]:
        c.append(a[i,:])
        np_arr = np.array(c)
    else:
        d = d+1

cv2.imwrite("test.png", np_arr)

a1 = np.array(np_arr)
demo1 = (max(a1.sum(axis=0))*0.98) > a1.sum(axis=0)
# counter = collections.Counter(demo1)
# print(counter.most_common(3))
d=0
c = []
t1, t2 = a1.shape
for i in range(t2):
    if demo1[i]:
        c.append(a1[:, i])
        np_arr2 = np.array(c)
    else:
        d = d+1
np_arr2 = np_arr2.transpose()
cv2.imwrite("test1.png", np_arr2)




# import cv2
#
# img = cv2.imread(r'\\172.16.0.6\cat\Charts\PNG Image\letterHeadIssues\13665608_0073.png')
# mser = cv2.MSER_create()
#
# #Resize the image so that MSER can work better
# img = cv2.resize(img, (img.shape[1]*2, img.shape[0]*2))
#
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# vis = img.copy()
#
# regions = mser.detectRegions(gray)
# hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions[0]]
# cv2.polylines(vis, hulls, 1, (0,255,0))
#
# cv2.namedWindow('img', 0)
# cv2.imshow('img', vis)
#
#
# cv2.imwrite("test.png",vis)
# while(cv2.waitKey()!=ord('q')):
#     continue
# cv2.destroyAllWindows()
