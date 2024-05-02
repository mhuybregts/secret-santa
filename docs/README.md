# Secret Santa

Secret Santa tool with email capabilities. This tools lets a user add an arbitrary number of people, providing them each with a name and email, and matching them up at random. The participants will then receive an email, telling them who they got for secret santa. You can also specify that certain people should not be able to get certain other people. The program will let you know if it was unable to generate a match for everyone, and will prompt you to try again.

## Email Information

Using Python to send emails: https://realpython.com/python-send-email/

> Information regarding the account used to send emails is to be included in secret_santa.conf

## Config File Format

```conf
# Email Settings
[Email]
email = "Enter the email you want to use"
app_password = "Generate an app password for the email"
smtp_port = 465

[GUI]
# If you update this field, make sure to update the home_url as well
gui_port = 9000
home_url = http://localhost:9000/index.html
```
