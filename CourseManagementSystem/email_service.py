import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD

def send_email(to_email, subject, body):
    """Send an email using the SMTP server."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(EMAIL_USER, EMAIL_PASSWORD)  # Log in to the email server
            server.send_message(msg)  # Send the email
            print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email and app password.")
    except Exception as e:
        print(f"An error occurred: {e}")