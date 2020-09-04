import os
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail:

    def __init__(self):
        self.mail_user = os.environ.get('EMAIL_USER')
        self.mail_password = os.environ.get('EMAIL_PASS')
        self.receiver_address = 'furkan.cetin1@yandex.com'



    def send_mail(self, message):
        """
        This function takes string and sends mail to the receiver_address
        """

        #if you want to add attachment(image, pdf) youtube video explains it
        #excel attachment example https://stackoverflow.com/a/60972152
        #How to send e-mail https://www.youtube.com/watch?v=JRCJ6RtE3xU
        msg = MIMEMultipart()
        msg['Subject'] = 'About your product list'
        msg['From'] = self.mail_user
        msg['To'] = self.receiver_address    #if you want to send multiple address make a list of mails 
        msg.attach(MIMEText(message, "html"))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.mail_user, self.mail_password)

            smtp.send_message(msg)

    def create_seller_tags(self, product_links):
        """
        This function takes seller and links dictionary and creates html link tags
        dictionary format {seller:link}
        """
        links_html = ''

        for seller in product_links:
            links_html += f'<br><a href="{product_links[seller]}">{seller}</a><br>'
        
        return links_html


    def create_mail_body(self, product_name, discount_link, product_links):
        """
        This function creates body of the mail
        """
        
        msg = f"""\
        <html>
        <body>
            <p>Hi Furkan,<br>
            <br> There could be a discount opportunity for the product you follow: <a href="{discount_link}">{product_name}</a> <br>
            <br> You can check prices from other sellers:<br>
            {self.create_seller_tags(product_links)}
            <br>Good Luck !<br>
            </p>
        </body>
        </html>
        """

        return msg