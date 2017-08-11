import RPi.GPIO as GPIO
import RPi.GPIO as GPIO
import datetime as dt
import picamera
import time
import tty, sys

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


fromaddr = "FROM EMAIL ADDRESS"
toaddr = "TO EMAIL ADDRESS"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "SUBJECT OF THE EMAIL"

body = "TEXT YOU WANT TO SEND"

msg.attach(MIMEText(body, 'plain'))


camera = picamera.PiCamera()
timestring=dt.datetime.now().strftime('%H:%M:%S:%d:%m:%Y')
ImageName = timestring + '.jpg'
camera.start_preview()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        input_state = GPIO.input(18)
        if input_state==False:
            camera.capture(ImageName)
            filename = timestring
            attachment = open("/home/pi/" + ImageName, "rb")

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "PASSWORD")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

            print('pressed')
            time.sleep(1)
