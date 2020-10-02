import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import from_email, password


msg = MIMEMultipart()
msg['Subject'] = 'Bere'
to_email = '105@rinova.ru'
message = 'test message'


msg.attach(MIMEText(message, 'plain'))
server = smtplib.SMTP('smtp.yandex.ru:465')
server.starttls()
server.login(from_email, password)
server.sendmail(from_email, to_email, msg.as_string())
server.quit()