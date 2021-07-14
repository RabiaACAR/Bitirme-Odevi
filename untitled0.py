import os, sys
import time
import numpy as np #matematiksel işlemler için
import cv2 #yüz belirleme ve diğer görüntü işlemleri için
import dlib #burun ağız çene noktaları tespiti
import math#kare alma vs. için
import tkinter as tk
#from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import smtplib#sonucu mail olarak gönderebilmek için
import mimetypes
from email.message import EmailMessage
from math import degrees



global imagepath
global shape 


directory='.\\FaceShape-master'

#directory klasörü yooksa oluştur.
if not os.path.exists(directory):
    os.makedirs(directory)

#imagepath = "kalp3.jpg"


#done()
def islem():
    image = cv2.imread(imagepath)
    width=image.shape[1]
    height = image.shape[0]
    image = cv2.resize(image, (width,height)) 
    image= cv2.putText(image, "d'ye basin.", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2, cv2.LINE_AA)
    cv2.imshow("Secilen resim",image)
    if cv2.waitKey(0) & 0xFF ==ord('d'):
        cv2.destroyAllWindows()
    detector()
    
def dosyaSec():
    global imagepath
    filename= filedialog.askopenfilename(initialdir=os.getcwd(), title="Dosya Seç", 
                    filetypes=(("jpg images", ".jpg"),("png images",".png"),("all files","*.*")))
    if not filename:
        pass
    imagepath=filename
    print(imagepath)
    
    
    
    islem()

def detector():
    detector = dlib.get_frontal_face_detector()

    predictor = dlib.shape_predictor("shape_predictor_81_face_landmarks.dat")

    image = cv2.imread(imagepath)
    width=image.shape[1]#görüntünün genişliğini almak için
    height = image.shape[0]#görüntünün yüksekliğini almak için
    #image = cv2.resize(image, (675,750))
    results= image


    gray =  cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
    gray=image
    faces = detector(gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        landmarks = predictor(image=gray, box=face)
        for n in range(0,81):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
        #cv2.circle(img=img, center=(x,y), radius=3, color=(0,255,0), thickness=-1)
   
        
   
        
    
      

        face_X=pow(landmarks.part(71).x - landmarks.part(71).y,2)
        face_y=pow(landmarks.part(8).x - landmarks.part(8).y,2)
        faceLength=face_X+face_y
        faceLength=math.sqrt(faceLength)
        faceLength=(faceLength/20)

    
    
        forehead_X=pow(landmarks.part(68).x - landmarks.part(68).y,2)
        forehead_y=pow(landmarks.part(74).x - landmarks.part(74).y,2)
        forehead=forehead_X+forehead_y
        foreheadWidth=math.sqrt(forehead)
        foreheadWidth=(foreheadWidth/20)
        print("Forehead length = ",foreheadWidth)
    
    
        jawline_X=pow(landmarks.part(3).x - landmarks.part(3).y,2)
        jawline_y=pow(landmarks.part(8).x - landmarks.part(8).y,2)
        jawlineLength=jawline_X+jawline_y
        jawlineLength=math.sqrt(jawlineLength)
        jawlineLength=(jawlineLength/20)
        print("jawline length = ",jawlineLength)
        
    
    
    
        cheekbone_X=pow(landmarks.part(26).x - landmarks.part(26).y,2)
        cheekbone_y=pow(landmarks.part(17).x - landmarks.part(17).y,2)
        cheekboneLength=cheekbone_X+cheekbone_y
        cheekboneLength=math.sqrt(cheekboneLength)
        cheekboneLength=(cheekboneLength/20)
        print("cheekbone length = ",cheekboneLength)
    
       
    
        
          
        if((foreheadWidth > cheekboneLength) and (cheekboneLength > jawlineLength)  ):
            shape='KALP'
            oneri=cv2.imread("kalp_oneri.jpg")
            oneri2="kalp_oneri.jpg"

   
        elif((faceLength > jawlineLength) and (math.isclose(cheekboneLength, foreheadWidth, abs_tol=0.5)) and (math.isclose(jawlineLength, foreheadWidth, abs_tol=0.5))  ):
             shape='DIKDORTGEN'
             oneri=cv2.imread("dikdortgen_oneri.jpg")
             oneri2="dikdortgen_oneri.jpg"

      


        elif((faceLength > cheekboneLength) and (math.isclose(cheekboneLength, foreheadWidth, abs_tol=0.5)) and (cheekboneLength > jawlineLength)) :
            shape='Oval'
            oneri=cv2.imread("oval_oneri.jpg")
            oneri2="oval_oneri.jpg"

   
        elif((math.isclose(faceLength, cheekboneLength, abs_tol=0.5)) and (cheekboneLength > foreheadWidth) and (math.isclose(foreheadWidth, jawlineLength, abs_tol=0.5))):
            shape='YUVARLAK'
            oneri=cv2.imread("yuvarlak_oneri.jpg")
            oneri2="yuvarlak_oneri.jpg"


        elif((math.isclose(cheekboneLength, faceLength, abs_tol=0.5)) and (math.isclose(cheekboneLength, foreheadWidth, abs_tol=0.5)) and (math.isclose(jawlineLength, foreheadWidth, abs_tol=0.5)) ):
            shape='KARE'
            oneri=cv2.imread("kare_oneri.jpg")
            oneri2="kare_oneri.jpg"

   
        else:
            print("TEKRAR DENEYİNİZ")
    
    
        img1=cv2.putText(results, shape, (20, 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),1, cv2.LINE_AA)
        img1 = cv2.resize(img1,(width,height))
        img2 = cv2.resize(oneri,(width, height))
        results = np.hstack((img1,img2))
        cv2.imshow('Yuz sekli ve cerceveler',results)
        
        mail_adresi=mailgiris.get()
       

        message = EmailMessage()
        gonderen= 'rabiaaaacar@gmail.com'
        alici = mail_adresi
        message['From'] = gonderen
        message['To'] = alici
        message['Subject'] = 'Yüz şekli belirleme ve çerçeve önerisi'
        body = """Merhaba, yüz şeklin için önerdiğimiz çerçeveler ektedir :)"""
        message.set_content(body)
        mime_type, _ = mimetypes.guess_type(oneri2)
        mime_type, mime_subtype = mime_type.split('/')
        with open(oneri2, 'rb') as file:
            message.add_attachment(file.read(),
            maintype=mime_type,
            subtype=mime_subtype,
            filename= oneri2)
        print(message)
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
        mail_server.set_debuglevel(1)
        mail_server.login('mail', 'şifre')
        mail_server.send_message(message)
        mail_server.quit()
        
    


        cv2.waitKey()
    
def VideoDet():
    global imagepath
    videoimage=cv2.VideoCapture(0)
    while True:
        ret, frame=videoimage.read()
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
        
            imgname=directory+"\\IMG"+ datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            cv2.imwrite(imgname,frame)
            cv2.destroyAllWindows()
            break
    imagepath=imgname
    
    
    
    
    islem()

# def exit_():
#     pencere.destroy()
#     sys.exit()



pencere=Tk()
pencere.title("Yüz Şekli Tespiti")

img = ImageTk.PhotoImage(file="home1.jpg")
width, height = img.width(), img.height()
canvas = tk.Canvas(pencere, width=width, height=height)
canvas.pack()
canvas.create_image((0, 0), image=img, anchor="nw")

mailname=tk.Label(text="Mail",font="Arial 12 bold")
mailname.place(x=350, y=100)
mailgiris=tk.Entry(width=30, borderwidth=3)
mailgiris.place(x=400, y=100)


dosyasec=tk.Button( borderwidth=2,  width=24, text='Fotoğraf seç', command=dosyaSec)
dosyasec.place(x=100, y=270)



videodet=tk.Button(borderwidth=2,  width=24, text='Video', command=VideoDet)
videodet.place(x=400, y=270)

cikis=tk.Button(borderwidth=2, width=24, text='Çıkış', command=pencere.destroy)

cikis.place(x=700, y=270)





pencere.mainloop()