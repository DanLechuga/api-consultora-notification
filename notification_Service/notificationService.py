from notification_middleware.dto.request import sendNotification
import smtplib
import os
from email.message import EmailMessage
import ssl

def getVariable(name):
    return os.environ.get(name,"NOT FOUND")


async def sendMail(notification : sendNotification.sendNotification):
    destinatario = getVariable("user")
    asunto = "Contacto para cotizacion de proyecto"
    emailMessages = EmailMessage()
    emailMessages['From'] = notification.email
    emailMessages['To'] = destinatario
    emailMessages['Subject'] = asunto
    msj = f"Posible cliente con identificaciones \n email: {notification.email},\n numero de telefono: {notification.phoneNumber} \n envio el siguiente mensaje "
    msj = msj + str(notification.message)
    emailMessages.set_content(msj)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context= context) as smtp:
        smtp.login(destinatario,getVariable("keyGmail"))
        smtp.sendmail(str(notification.email),destinatario,emailMessages.as_string())
    