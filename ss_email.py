from http.server import BaseHTTPRequestHandler as RequestHandler, HTTPServer as Server
from urllib.parse import parse_qs
import smtplib, ssl

SMTP_PORT = 465
EMAIL = 'no.reply.secret.santa.25@gmail.com'

context = None
password = None

class CommandHandler(RequestHandler):

    def do_POST(self):
        if self.path == '/send_email':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)

            # Get information from the request
            recipient = data['recipient'][0]
            message = data['message'][0]

            # Login and send email
            with smtplib.SMTP_SSL('smtp.gmail.com', SMTP_PORT, context=context) as server:
                server.login(EMAIL, password)
                server.sendmail(EMAIL, recipient, message)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()



if __name__ == '__main__':    
    
    password = input('Enter App Password: ')
    context = ssl.create_default_context()

    server_address = ('', 9000)  # Replace 9000 with your desired port
    httpd = Server(server_address, CommandHandler)
    print('Server is running...')
    httpd.serve_forever()
