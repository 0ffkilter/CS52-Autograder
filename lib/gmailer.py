from __future__ import print_function

import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httplib2
import oauth2client
from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools

import codecs


class cmd_flags(object):
    def __init__(self):
        self.short_url = True
        self.noauth_local_webserver = False
        self.logging_level = 'ERROR'
        self.auth_host_name = 'localhost'
        self.auth_host_port = [8080, 8090]


class GoogleMailer(object):
    """Basic mailer class to take advantage of Google's Python API"""

    def __init__(self):
        # builds the Gmail service object
        # Note that we are passing it None, so any API docs about
        # regarding run flags will be useless!
        # It would be good to fix this, but due to clashes with other script
        # parsers, I have not.
        self._service = self._build_gmail_service(None)

    def send_email(self, sender, to, subject, message, html=None,
                   attachment=None):
        """Builds and sends an email.

        :param sender: sender's address
        :param to: recipient's address
        :param subject: subject line of email
        :param message: text to appear in the body of the email
        :return: google message dictionary if successful, None otherwise
        """
        if html:
            content = self._create_html_message(sender, to, subject, message,
                                                html, attachment)
        else:
            content = self._create_message(sender, to, subject, message,
                                           attachment)

        return self._send_message(content)

    def _build_gmail_service(self, flags):
        """Build a basic service for use with Gmail

        :param flags: command line flags
        :return: a gmail service object
        """
        credential_dir = os.path.join(os.path.expanduser("~"))

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-u-grade.json')

        print('Your credentials are stored: %s' % (credential_path))
        print(
              'If you would like to destroy the credentials, delete this file run:')
        print('\t rm %s' % (credential_path))

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            # get user input of gmail credential file
            api_creds = input('Path to Gmail Credentials: ')
            flow = client.flow_from_clientsecrets(api_creds,
                                                  'https://www.googleapis.com/auth/gmail.send')
            flow.user_agent = 'CLI'
            credentials = tools.run_flow(flow, store, cmd_flags())
            # credentials = tools.run(flow, store)#tools.run_flow(flow, store, flags)

        http = credentials.authorize(httplib2.Http())

        return discovery.build('gmail', 'v1', http=http)

    def _send_message(self, message):
        """Send a message from logged in account.

        :param message: MIME message
        :return: message if successful, None if failed
        """
        try:
            message = (self._service.users()
                       .messages().send(userId='me', body=message).execute())
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def _create_message(self, sender, to, subject, message_text,
                        attach_path=None):
        """Create a simple MIMEText message for an email.

        :param sender: sender's email address
        :param to: recipient's email address
        :param subject: subject line of the email
        :param message_text: message body
        """
        message = MIMEMultipart('alternative')
        plain = MIMEText(message_text, 'plain')
        message.attach(plain)

        if attach_path:
            tmpmsg = message
            message = MIMEMultipart()
            message.attach(tmpmsg)
            content_type, encoding = mimetypes.guess_type(attach_path)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = codecs.open(attach_path, 'rb', encoding='utf-8', errors='ignore')
                attach = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(attach_path, 'rb')
                attach = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(attach_path, 'rb')
                attach = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(attach_path, 'rb')
                attach = MIMEBase(main_type, sub_type)
                attach.set_payload(fp.read())
                fp.close()

            attach.add_header('Content-Disposition', 'attachment',
                              filename=os.path.basename(attach_path))
            message.attach(attach)

        message['To'] = to
        message['From'] = sender
        message['Subject'] = subject

        b = message.as_bytes()
        b64 = base64.urlsafe_b64encode(b)
        return {'raw': b64.decode()}

    def _create_html_message(self, sender, to, subject, text, html,
                             attach_path=None):
        message = MIMEMultipart('alternative')
        html = MIMEText(html, 'html')
        plain = MIMEText(text, 'plain')
        message.attach(plain)
        message.attach(html)

        if attach_path:
            tmpmsg = message
            message = MIMEMultipart()
            message.attach(tmpmsg)
            content_type, encoding = mimetypes.guess_type(attach_path)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(attach_path, 'rb')
                attach = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(attach_path, 'rb')
                attach = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(attach_path, 'rb')
                attach = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(attach_path, 'rb')
                attach = MIMEBase(main_type, sub_type)
                attach.set_payload(fp.read())
                fp.close()

            attach.add_header('Content-Disposition', 'attachment',
                              filename=os.path.basename(attach_path))
            message.attach(attach)

        message['To'] = to
        message['From'] = sender
        message['Subject'] = subject

        return {'raw': base64.urlsafe_b64encode(
                message.as_string())}
