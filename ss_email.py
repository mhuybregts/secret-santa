from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import smtplib, ssl
import configparser
import webbrowser

CONFIG_FILE = 'secret_santa.conf'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

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

            smtp_server.sendmail(config['Email']['email'], recipient, message)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

if __name__ == '__main__':    
    
    context = ssl.create_default_context()
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', int(config['Email']['smtp_port']), context=context)
   
    try:
        smtp_server.login(user=config['Email']['email'], password=config['Email']['app_password'])
    except smtplib.SMTPAuthenticationError: 
        print('Invalid Credentials, Update Config File')
        exit(0)
    
    server_address = ('', int(config['GUI']['gui_port']))  # Replace 9000 with your desired port
    httpd = HTTPServer(server_address, CommandHandler)
    
    print('HTTP Server is Running...')
    webbrowser.open(config['GUI']['home_url'])
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Exiting...')
        smtp_server.close()
        exit(0)
