from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from customlog import custom_logger

HOST = "smtp.gmail.com"
SENDER = "gibrailtester@gmail.com"
PASSWORD = "cdtxqlmyrphojemu"
PORT = "587"    
SUBJECT = "AUTH NOTIFICATION"

def create_msg(client: str):
    msg = MIMEMultipart()
    msg['from'] = SENDER
    msg['to'] = client
    msg['subject'] = SUBJECT
    msg_body = f"""
        Hello {client}
        <a href="google.com"> link </a>
    """
    html_body = MIMEText(msg_body, "html")
    msg.attach(html_body)
    return msg

def send_msg(msg: MIMEMultipart, client: str):
    try:
        custom_logger.info(client)
        conn = smtplib.SMTP(HOST)
        conn.connect(HOST, PORT)
        conn.ehlo()
        conn.starttls()
        conn.ehlo()
        conn.set_debuglevel(False)
        conn.login(user=SENDER, password=PASSWORD)
        try:
            conn.sendmail(SENDER, client, msg.as_string())
        finally:
            conn.close()
    except Exception as e:
        custom_logger.info(e)
        print("error occure with: %s" % e)