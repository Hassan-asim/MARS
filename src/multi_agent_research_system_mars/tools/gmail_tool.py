import os
import base64
import json
from email.mime.text import MimeText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Type, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import sys
import os

# Load environment variables
config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'config.env')
load_dotenv(config_path)


class GmailToolInput(BaseModel):
    """Input schema for Gmail tool."""
    to_email: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")
    attachments: Optional[list] = Field(default=None, description="List of file paths to attach")


class GmailTool(BaseTool):
    name: str = "Gmail Email Sender"
    description: str = (
        "Send emails using Gmail API. Can send plain text emails with attachments. "
        "Requires recipient email, subject, and body content."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def __init__(self):
        super().__init__()
        self.service = self._authenticate_gmail()

    def _authenticate_gmail(self):
        """Authenticate and return Gmail service object."""
        try:
            # Create credentials from environment variables
            creds_info = {
                "client_id": os.getenv('GMAIL_CLIENT_ID'),
                "client_secret": os.getenv('GMAIL_CLIENT_SECRET'),
                "refresh_token": os.getenv('OAUTH_REFRESH_TOKEN'),
                "type": "authorized_user"
            }
            
            creds = Credentials.from_authorized_user_info(creds_info, ['https://www.googleapis.com/auth/gmail.send'])
            
            # Refresh the token if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            # Build the Gmail service
            service = build('gmail', 'v1', credentials=creds)
            return service
            
        except Exception as e:
            print(f"Error authenticating Gmail: {str(e)}")
            return None

    def _create_message(self, to_email: str, subject: str, body: str, attachments: Optional[list] = None):
        """Create email message."""
        try:
            # Create message
            message = MIMEMultipart()
            message['to'] = to_email
            message['from'] = os.getenv('SENDER_EMAIL')
            message['subject'] = subject

            # Add body
            message.attach(MIMEText(body, 'plain'))

            # Add attachments if provided
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        message.attach(part)

            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            return {'raw': raw_message}
            
        except Exception as e:
            print(f"Error creating message: {str(e)}")
            return None

    def _run(self, to_email: str, subject: str, body: str, attachments: Optional[list] = None) -> str:
        """Send email using Gmail API."""
        try:
            if not self.service:
                return "Error: Gmail authentication failed. Please check your credentials."

            # Create the message
            message = self._create_message(to_email, subject, body, attachments)
            if not message:
                return "Error: Failed to create email message."

            # Send the message
            result = self.service.users().messages().send(
                userId='me', 
                body=message
            ).execute()

            return f"Email sent successfully! Message ID: {result.get('id')}"

        except Exception as e:
            return f"Error sending email: {str(e)}"


# Create an instance of the tool for easy import
gmail_tool = GmailTool()
