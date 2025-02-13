import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

class EmailSender:
    def __init__(self, gmail_user: str, gmail_password: str):
        """
        Generic email sender class using Gmail SMTP.
        Note: For Gmail, you need to use an App Password, not your regular password.
        Generate one at: https://myaccount.google.com/apppasswords
        """
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password

    def send_email(self, 
                  recipients: List[str], 
                  subject: str, 
                  body: str,
                  sender_name: str = None,
                  is_html: bool = False) -> bool:
        """
        Send email to specified recipients
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            body: Email body content
            sender_name: Optional sender name to show instead of email
            is_html: Whether the body content is HTML
        """
        msg = MIMEMultipart('alternative')
        from_header = f"{sender_name} <{self.gmail_user}>" if sender_name else self.gmail_user
        msg['From'] = from_header
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        
        # Attach the body with the appropriate type
        content_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, content_type, 'utf-8'))

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.close()
            
            print(f"Email sent successfully to {len(recipients)} recipients")
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False 