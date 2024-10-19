import smtplib

SMTP_SERVER = "smtp.gmx.com"
SMTP_PORT = 587
EMAIL_USER = "piurkowski@gmx.com"  # Your GMX email
EMAIL_PASSWORD = "21619062Mz@"  # Your app password

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Upgrade to secure connection
        server.login(EMAIL_USER, EMAIL_PASSWORD)  # Authenticate
        print("Login successful!")
except smtplib.SMTPAuthenticationError:
    print("Authentication failed. Please check your email and password.")
except Exception as e:
    print(f"An error occurred: {e}")