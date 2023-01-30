from os import execle
import smtplib
from email.mime.text import MIMEText
from dataclasses import dataclass
from string import Template
import traceback
from pydantic import BaseModel, AnyUrl
from pydantic.networks import EmailStr


# @dataclass
class DagMailConfig(BaseModel):
    host: str
    port: int
    user: EmailStr
    password: str


class DagMail:
    mail_server = None
    sender: str
    receivers = []

    def __init__(self, config: DagMailConfig) -> None:
        self.config = config
        self.sender = self.config.user

    def __enter__(self):
        self.create_server()
        print("mail server creato")
        self.login()
        return self

    def __exit__(self, exception_type, exception_value, tb):
        self.mail_server.quit()
        if exception_type is not None:
            # traceback.print_exception( exception_type, exception_value, tb)
            return False  # uncomment to pass exception through
        return True

    def create_server(self):
        print("creazione del mails server ...")
        self.mail_server = smtplib.SMTP_SSL(
            host=self.config.host, port=self.config.port
        )
        return self

    def login(self):
        print("login to mail server....")
        self.mail_server.login(self.config.user, self.config.password)
        return self

    # opzionale
    def set_sender(self, address: str = None):
        self.sender = self.config.user if not address else address
        print("aggiunto mittente...")
        return self

    def add_receiver(self, address):
        self.receivers.append(address)
        print("aggiunto destinatatio...")
        return self

    def messageHTML(self, body, subject):
        self.msg = MIMEText(body, "html")
        self.msg["Subject"] = subject
        self.msg["From"] = self.sender
        self.msg["To"] = ", ".join(self.receivers)
        return self

    def send(self):
        err = self.mail_server.sendmail(
            self.sender, self.receivers, self.msg.as_string()
        )
        print("messaggio inviato")
        return err


# config = DagMailConfig(
#     host='mail.flatmac.com',
#     port=465,
#     user="dag@flatmac.com",
#     password=''
# )

# my_template = Template('My Name is $x')
# my_template.substitute({'x': "saima"})

# body = "Ciao <strong>Python</strong>"

# try:
#     with DagMail(config) as ms:
#         ms.add_receiver('user@gmail.com')
#         ms.add_receiver('user@gmail.com')
#         ms.messageHTML(body, "invio della classe python")
#         ms.send()
# except Exception as e:
#     print(str(e))

# oppure

# ms = DagMail(config)
# ms.create_server()
# ms.login()
# ms.add_receiver("address")
# ms.set_sender("sender@address")
# ms.messageHTML(body, "subject")
# ms.send()

#####################################################################
# oppure alal vecchia maniera

# sender = "dag@flatmac.com"
# receivers = ['user@gmail.com']
# body = "Ciao <strong>Python</strong>"

# msg = MIMEText(body, 'html')
# msg['Subject'] = 'python'
# msg['From'] = sender
# msg['To'] = ', '.join(receivers)

# mail_server = smtplib.SMTP_SSL(host='mail.flatmac.com', port=465)
# mail_server.login(user='dag@flatmac.com', password='')
# mail_server.sendmail(sender, receivers, msg.as_string())
# mail_server.quit()
