from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import smtplib, ssl
import webbrowser

SMTP_PORT = 465
EMAIL = 'no.reply.secret.santa.25@gmail.com'
HOME_URL = 'http://localhost:9000/index.html'

smtp_server = None

class CommandHandler(SimpleHTTPRequestHandler):
    
    def do_POST(self):
        if self.path == '/send_email':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = parse_qs(post_data)

            # Get information from the request
            recipient = data['recipient'][0]
            message = data['message'][0]

            smtp_server.sendmail(EMAIL, recipient, message)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

if __name__ == '__main__':    
    
    context = ssl.create_default_context()
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', SMTP_PORT, context=context)
   
    while True:
        password = input('Enter App Password: ')
        try:
            smtp_server.login(user=EMAIL, password=password)
            break
        except smtplib.SMTPAuthenticationError: 
            print('Invalid Credentials, Try Again')

    
    server_address = ('', 9000)  # Replace 9000 with your desired port
    httpd = HTTPServer(server_address, CommandHandler)
    
    print('HTTP Server is Running...')
    webbrowser.open(HOME_URL)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Exiting...')
        smtp_server.close()
        exit(0)
