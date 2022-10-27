# SMSTexter
Utility written in Python to send texts to a number or many numbers from a specified email address

Based on Twilio API
Secure data is stored in Constants.py, unversioned file only stored locally
Sends emails to text-to-email service using SMTPLib
Has CSV tracking different cell carriers and their text-to-email address
Caches numbers and their cell carriers locally in cached-carriers.json
