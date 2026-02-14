import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage


load_dotenv()


# Use SMTP, Send formatted email, 📧 Notification Service
class EmailAgent:

    def send_email(self, subject, body):
        
        try:
            msg = EmailMessage()
            msg["From"] = os.getenv("EMAIL_USER")
            msg["To"] = os.getenv("EMAIL_RECEIVER")
            msg["Subject"] = subject
            msg.set_content(body)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(
                    os.getenv("EMAIL_USER"),
                    os.getenv("EMAIL_PASSWORD")
                )
                server.send_message(msg)

            return True
        
        except Exception as e:
            print("EMAIL ERROR:", e)
            return False
        
        
