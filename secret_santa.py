from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import smtplib
import ssl
from email.message import EmailMessage
import configparser
import webbrowser

config = configparser.ConfigParser()
config.read('secret_santa.conf')

smtp_server = None


class CommandHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/send_email':
            # Parse request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)

            message = f"Hello {data['person'][0]},\n\n" \
                f"You have gotten {data['match'][0]} "\
                "for Secret Santa!\nMake sure you keep "\
                "it a secret (and get a good gift).\n\n" \
                "Merry Christmas"

            # Construct email message from request data
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = 'Let\'s see who you got for Secret Santa!'
            msg['From'] = config['Email']['email']
            msg['To'] = data['address'][0]

            smtp_server.send_message(msg)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()


if __name__ == '__main__':

    context = ssl.create_default_context()
    smtp_server = smtplib.SMTP_SSL(config['Email']['smtp_server'],
                                   int(config['Email']['smtp_port']),
                                   context=context)

    try:
        smtp_server.login(user=config['Email']['email'],
                          password=config['Email']['password'])
    except smtplib.SMTPAuthenticationError as e:
        print(e)
        print('Invalid Credentials, Update Config File')
        exit(0)

    server_address = ('', int(config['GUI']['gui_port']))
    httpd = HTTPServer(server_address, CommandHandler)

    print('HTTP Server is Running...')
    webbrowser.open(config['GUI']['home_url'])

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Exiting...')
        smtp_server.close()
        exit(0)
