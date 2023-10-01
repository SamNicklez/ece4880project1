import smtplib

# Dictionary of valid carriers and their respective email extensions
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com",
    "uscellular": "@email.uscc.net"
}

# Email and password that are used to send text alerts
EMAIL = "lukefarmer6801@gmail.com"  # Replace with your Gmail email
PASSWORD = "rwvrxfqqvcykrskr"  # Replace with your Gmail password


# Function send_message sends text to input phone number, carrier, and message
def send_message(phone_number: int, carrier: str, message: str):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, message)
