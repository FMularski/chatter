import smtplib
from . import email_pass


class EmailManager:

    @staticmethod
    def send_message(to, message):
        mail_conn = smtplib.SMTP('smtp.gmail.com', 587)
        mail_conn.ehlo()
        mail_conn.starttls()
        mail_conn.login(email_pass.login, email_pass.password)

        mail_conn.sendmail(email_pass.login, to, message)
        mail_conn.quit()
