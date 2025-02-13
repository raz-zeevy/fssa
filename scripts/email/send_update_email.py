from dotenv import load_dotenv
from email_sender import EmailSender
from git_update_notifier import GitUpdateNotifier
import os
from typing import List

def load_recipients(file_path: str) -> List[str]:
    """Load email recipients from a file"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    # Load environment variables
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not gmail_user or not gmail_password:
        print("Error: Gmail credentials not found in environment variables")
        print("Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables")
        return

    # Initialize services
    email_sender = EmailSender(gmail_user, gmail_password)
    notifier = GitUpdateNotifier(email_sender)
    
    # Load recipients
    recipients = load_recipients(os.path.join(os.path.dirname(__file__), 'config/email_recipients.txt'))
    
    # Send the notification
    notifier.send_update_notification(recipients)

if __name__ == "__main__":
    load_dotenv()
    main() 