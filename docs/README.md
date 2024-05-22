# Secret Santa

Secret Santa tool with email capabilities. This tools lets a user add an arbitrary number of people, providing them each with a name and email, and matching them up at random. The participants will then receive an email, telling them who they got for secret santa. You can also specify that certain people should not be able to get certain other people. The program will let you know if it was unable to generate a match for everyone, and will prompt you to try again.

## Email Information

Using Python to send emails: https://realpython.com/python-send-email/

Generating app passwords in gmail: https://support.google.com/mail/answer/185833?hl=en

> Information regarding the account used to send emails is to be included in secret_santa.conf

## Config File Format

```conf
# Email Settings
[Email]
smtp_server = <Enter the name of the SMTP server>
email = <Enter the email address you want to use>
app_password = <Enter the password for the email address> # Use an app password for gmail
smtp_port = 465

[GUI]
# If you update this field, make sure to update the home_url as well
gui_port = 9000
home_url = http://localhost:9000/index.html
```

## How to run

Run [secret_santa.py](/secret_santa.py), a web browser will open where you can enter the names and email addresses
of the people you want to include
