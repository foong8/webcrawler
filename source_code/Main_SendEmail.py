import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
mail_content = '''Hello,
This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
Thank You'''


from pathlib import Path
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import encoders

#The mail addresses and password
sender_address      = 'stock.volume.spike@gmail.com'
sender_pass         = '1234567890@abcdefg'
receiver_address    = 'stock.volume.spike@gmail.com'
subject_title       = "Today Vol Spike"
attachment_filepath = r"C:\Users\User\Documents\AlgoTrading\master_list\Process_MalaysiaStock_MasterLists.csv"


def main():
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject_title
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    
    part = MIMEBase('application', "octet-stream")
    with open(attachment_filepath, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(Path(attachment_filepath).name))
    message.attach(part)


    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


if __name__ == "__main__":
    main()
