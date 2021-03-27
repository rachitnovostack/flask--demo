import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def send_mail(email_id,url):
    
    msg_to_send = 'Please Click on the below link to reset your password. The link is valid only for ONE hour.'
    # Python code to illustrate Sending mail from 

    import smtplib 
    MAIL_USERNAME='ckdss.admin@techstax.ml'
    MAIL_PASSWORD='DNXs$?ejp$5'

    MAIL_SERVER = 'smtp.hostinger.in'
    # creates SMTP session 
    s = smtplib.SMTP(MAIL_SERVER, 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(MAIL_USERNAME, MAIL_PASSWORD) 

    # message to be sent 
    msg = MIMEMultipart()

    msg['From'] = 'CK DSS Admin <admin@ckdss.tech>'
    msg['To'] = email_id
    msg['Subject'] = 'User Password Reset Request'

    body = msg_to_send +'\n'+url
    msg.attach(MIMEText(body,'plain'))
    text = msg.as_string()

    # sending the mail 
    s.sendmail(MAIL_USERNAME, email_id, text) 

    # terminating the session 
    s.quit() 
