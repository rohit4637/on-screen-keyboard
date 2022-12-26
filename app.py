import cv2
import mediapipe as mp
import time
import imutils
from pynput.keyboard import Key,Controller
ctime=time.time()

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

keynote=Controller()

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=4, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

keys=[['Q','W','E','R','T','Y','U','I','O','P',"<-"],
     ['A','S','D','F','G','H','J','K','L',':'],
     ['Z','X','C','V','B','N','M',',','.','/',"clr"],
     ["sp"]]


def drawALL(img,buttonLIST):
    for b in buttonLIST:
        x, y = b.pos
        w, h = b.size
        cv2.rectangle(img, b.pos, (x + w, y + h), (204, 204, 0), cv2.FILLED)
        cv2.putText(img, b.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    return img

class button:
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.text=text
        self.size=size
        
    def draw(self,img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (204, 204, 0), cv2.FILLED)
        cv2.putText(img, self.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        lastx=x + w
        lasty= y + h
        return img

buttonLIST=[]
for k in range(len(keys)):
    for i,ki in enumerate(keys[k]):
        buttonLIST.append(button([100*i+50,100*k+50],ki))
        
  
#print(buttonLIST)      
keytext=""
flag=0
lenrec=1000
lastx=0
lasty=0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    #cv2.imshow('img',frame)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result=hands.process(framergb)

    #frame = imutils.resize(frame, width=1050)
    #x, y, c = frame.shape
    #print(x, y)

    # bt=button([100,100],'Q')
    # frame=bt.draw(frame)
    
    # bt=button([500,100],'W')
    # frame=bt.draw(frame)
    
    frame=drawALL(frame,buttonLIST)
    
    
    
    if result.multi_hand_landmarks:
        
        for handslms in result.multi_hand_landmarks:
            landmarks = []
            for lm in handslms.landmark:
                # # print(id, lm)
                # print(lm.x)
                # print(lm.y)
                flag=1

                lmx = int(lm.x * 1280)
                lmy = int(lm.y * 720)
                #print(lmx,lmy)

                landmarks.append([lmx, lmy])
                # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
            
            #forefinge=landmarks[8][0]
            
            if landmarks:
                for button in buttonLIST:
                    x,y = button.pos
                    w,h = button.size
                    if x<landmarks[8][0]<x+w and y<landmarks[8][1] < y+h:
                        cv2.rectangle(frame, (x-5,y-5), (x + w +5, y + h +5), (204, 204, 0), cv2.FILLED)
                        cv2.putText(frame, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                        
                        indexF=(landmarks[8][0],landmarks[8][1])
                        thumbF=(landmarks[4][0],landmarks[4][1])
                        
                        
                        
                        if(abs(indexF[1]-thumbF[1]) < 50 and abs(indexF[0]-thumbF[0]) < 50):
                            cv2.rectangle(frame,(x-5,y-5), (x + w +5, y + h +5), (102, 255, 102), cv2.FILLED)
                            cv2.putText(frame, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                            if button.text=="<-":
                                keytext=keytext[:-1]
                                keynote.press(Key.backspace)
                                cv2.waitKey(300)
                            
                            elif button.text=="sp":
                                keytext+="_"
                                keynote.press(Key.space)
                                #keynote.press(" ")
                                cv2.waitKey(300)
                            
                            elif button.text=="clr":
                                keytext=""
                                cv2.waitKey(300)
                                
                            else:
                                keytext=keytext+button.text
                                keynote.press(button.text)
                                if(len(keytext)>20):
                                    #lenrec+=30
                                    lenrec=2000
                                cv2.waitKey(300)
                            #time.sleep(0.4)
            
                            
            pinkiF=(landmarks[20][0],landmarks[20][1])
            thumbF2=(landmarks[4][0],landmarks[4][1])
            
            if(abs(pinkiF[1]-thumbF2[1]) < 10 and abs(pinkiF[0]-thumbF2[0]) < 10):
                keytext=""
                        
    if(flag==1):       
        cv2.rectangle(frame, (100,350+100), (lenrec,450+100), (102, 255, 102), cv2.FILLED)
        cv2.putText(frame, keytext, (100, 425+100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)                    
                        
    print(lastx,lasty)
                            
    cv2.imshow('img',frame)


    if cv2.waitKey(1) == ord('q'):
        break
                    
cap.release()
cv2.destroyAllWindows()                       
                    
            
            
              

            
                
    
    


