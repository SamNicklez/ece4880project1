import smtplib
 
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com",
    "uscellular": "@email.uscc.net"
}
 
EMAIL = "lukefarmer6801@gmail.com"  # Replace with your Gmail email
PASSWORD = "rwvrxfqqvcykrskr"  # Replace with your Gmail password
 
def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)