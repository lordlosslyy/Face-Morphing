import numpy as np
import cv2
import pdb

# Read points from text file
def readPoints(path) :
    # Create an array of points.
    points = []
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))

    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha,ratioH,ratioS,ratioV) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))

    
    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []


    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))

    
    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0)
    
    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]
 #   pdb.set_trace()
    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    HSVrect = cv2.cvtColor(warpImage2, cv2.COLOR_BGR2HSV)
    H2, S2, V2 = cv2.split(HSVrect)
#    H=H*ratioH
#    S=S*ratioS
    V2=V2*np.sqrt(ratioV)
    #print(np.sqrt(ratioV)) 
    #S2=S2*(ratioS*alpha+ (1- alpha)/ratioS)

    for h in range(V2.shape[0]):
        for w in range(V2.shape[1]):
            if V2[h,w] >= 255:
                V2[h,w] = 255
            else:
                V2[h,w] = V2[h,w]

    
#
    HSVrect[:,:,0]=H2
    HSVrect[:,:,1]=S2
    HSVrect[:,:,2]=V2
    warpImage2 = cv2.cvtColor(HSVrect, cv2.COLOR_HSV2BGR)

    # Alpha blend rectangular patches

    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2
    
    HSVrect = cv2.cvtColor(imgRect, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSVrect)

    HSVwarp1 = cv2.cvtColor(warpImage1, cv2.COLOR_BGR2HSV)
    H_warp1, S_warp1, V_warp1= cv2.split(HSVwarp1)

    H = H_warp1

    HSVrect[:,:,0]=H
    HSVrect[:,:,1]=S
    HSVrect[:,:,2]=V
    imgRect = cv2.cvtColor(HSVrect, cv2.COLOR_HSV2BGR)
    # Copy triangular region of the rectangular patch to the output image
    img1[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]] = (img1[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]] * ( 1 - mask )  + imgRect * mask)

