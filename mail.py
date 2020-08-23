import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
RECEIVER_ADDRESS = 'furkan.cetin1@yandex.com'

def send_mail(message):
    """
    This function takes string and sends mail to the receiver_address
    """
    
    #if you want to add attachment(image, pdf) youtube video explains it
    #excel attachment example https://stackoverflow.com/a/60972152
    #How to send e-mail https://www.youtube.com/watch?v=JRCJ6RtE3xU
    msg = EmailMessage()
    msg['Subject'] = 'Grab dinner this weekend?'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_ADDRESS    #if you want to send multiple address make a list of mails 
    msg.set_content('How about dinner at 6 pm this Saturday?') 

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)

