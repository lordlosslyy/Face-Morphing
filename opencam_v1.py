import cv2



def opencam():
  cap = cv2.VideoCapture(0)

  # 設定影像的尺寸大小
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

  count=0 
  for i in range(2):
    
    print ("press q to take photo {0}".format(i+1))
    while(True):
      ret, frame = cap.read()
      cv2.imshow('frame', frame)   
      if cv2.waitKey(1) & 0xFF == ord('q'):
        if count == 0:
          cv2.imwrite("./images/ex1.jpg", frame)
          count=count+1
        else:
          cv2.imwrite("./images/ex2.jpg", frame)
        break
      
  cap.release()
  cv2.destroyAllWindows()