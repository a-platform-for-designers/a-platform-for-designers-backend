import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend


class NoTLSEmailBackend(DjangoEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)

    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(
                self.host, self.port, **self.connection_params
            )
            context = ssl._create_unverified_context()
            self.connection.ehlo()
            if self.use_tls:
                self.connection.starttls(context=context)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except smtplib.SMTPException as e:
            if not self.fail_silently:
                raise e
            return False
