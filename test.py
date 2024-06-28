import face_recognition
import imutils
import pickle
import time
import cv2
import os
import serial
import time
import threading 
import requests

from datetime import date


#import dropbox
#dropbox_access_token= "sl.BXeGA5Vx8TbUlrOz_2AH6ehz-Ck2w_VCCHSmbZpJClcxb1dFUECbiZBQzIP8ng1DX5TY2fYJ-oZjl3ky9GcumAOP3U1N9vzrghPqUm4ECJb5bSEtc9-4s0_xCvFxyy-w_Ka2O8n9ji4"    #Enter your own access token

#client = dropbox.Dropbox(dropbox_access_token)
#print("[SUCCESS] dropbox account linked")

arduino = serial.Serial( 'COM6', 9600, timeout=0.05)
sts=0
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data)
    return data

def close_door():
    global sts    
    sts=0
    write_read('c')
    print ("Closed")
    
#def upload_img(impath):
    
 #   dropbox_path= "/detection/"+impath
 #   computer_path=impath

    #try:
    #    client.files_upload(open(computer_path, "rb").read(), dropbox_path)
     #   print("[UPLOADED] {}".format(computer_path))
    #except:
   #     pass




import firebase_admin
from firebase_admin import credentials, storage, db, auth
from datetime import datetime

cred = credentials.Certificate('facedetection-c8549-firebase-adminsdk-1u8uu-4a3daf7e98.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'facedetection-c8549.appspot.com',
    'databaseURL':'https://facedetection-c8549-default-rtdb.firebaseio.com/'
})



storage = storage.bucket()



def upload_image_to_firebase_storage(image_path):
    # Generate a unique file name using the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    time = now.strftime("%Y%m%d")
    filename = f"{timestamp}.jpg"

    # Upload the image to Firebase Storage
    blob = storage.blob(filename)
    blob.upload_from_filename(image_path)

    # Get the public URL of the uploaded image
    email = "shravanssk12345@gmail.com"
    password ="ssk8491."
    #user = auth.sign_in_with_email_and_password(email, password)
    #url = storage.child(filename).get_url(user['idToken'])
    #url = blob.public_url
    
    #user = firebase_admin.auth.sign_in_with_email_and_password(email, password)
    #url = storage.blob(filename).get_url(user['idToken'])
    user = auth.get_user_by_email(email)
    cT= auth.create_custom_token(user.uid)
    url = storage.child(filename).get_url(cT)
    print(url)
    #return url, time

def upload_to_rtdb(url, timestamp):
    data = {
        "date" : timestamp,
        "url" : url
    }
    ref = db.reference("images").child("image").push().set(data)


def send_telegram_msg():
    TOKEN = "6142274739:AAGOWnbpWkWqzMqbFa3uZI3YrY8pjDM8KBM"
    
    chat_id = "5893637739"
    message = "An unknown person detected"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())
    print("message send")

    # Send the image file
    image_path = os.path.join("saved", "Unknown.jpg")
    files = {'photo': open(image_path, 'rb')}
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}"
    response = requests.post(url, files=files)
    print(response.json())
    print("Image sent successfully.")

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
# load the known faces and embeddings saved in last file
data = pickle.loads(open('face_model', "rb").read())
 
print("Streaming started")

video_capture = cv2.VideoCapture(0)
# loop over frames from the video file stream
cnt=0
while True:
    # grab the frame from the threaded video streamq
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
 
    # convert the input frame from BGR to RGB 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # the facial embeddings for face in input
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # loop over the facial embeddings incase
    # we have multiple embeddings for multiple fcaes
    for encoding in encodings:
       #Compare encodings with encodings in data["encodings"]
       #Matches contain array with boolean values and True for the embeddings it matches closely
       #and False for rest
        matches = face_recognition.compare_faces(data["encodings"],
         encoding)
        #set name =inknown if no encoding matches
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            #Find positions at which we get True and store them
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
            #set name which has highest count
            name = max(counts, key=counts.get)
            
 

        # update the list of names
        names.append(name)
        if(name!="Unknown" and sts==0):
            sts=1
            write_read('o')
            start_time = threading.Timer(10,close_door)
            start_time.start()
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
             0.75, (0, 255, 0), 2)
            
            pername="saved/"+name+".jpg"
            cv2.imwrite(pername,frame)
        
        if(name=="Unknown" and cnt%500==0):
            today = date.today()
            d1 = today.strftime("%d_%m_%Y")
            print("d1 =", d1)
            impath=d1+'.jpg'
            cv2.imwrite(impath,frame)
            
            #upload_img(impath)
            #send_telegram_msg()

            url, timestamp = upload_image_to_firebase_storage(impath)
            upload_to_rtdb(url, timestamp)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()