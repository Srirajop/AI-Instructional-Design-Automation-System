import os
import asyncio
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

async def test_email():
    load_dotenv(override=True)
    
    username = os.getenv("MAIL_USERNAME", "").strip()
    password = os.getenv("MAIL_PASSWORD", "").strip()
    password = password.replace(" ", "")

    config = ConnectionConfig(
        MAIL_USERNAME=username,
        MAIL_PASSWORD=password,
        MAIL_FROM=os.getenv("MAIL_FROM", username),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    message = MessageSchema(
        subject="e-Learning AI - Test Email",
        recipients=[os.getenv("MAIL_USERNAME")], # Send to self
        body="This is a test email.",
        subtype=MessageType.html
    )

    fm = FastMail(config)
    try:
        await fm.send_message(message)
        print("Test email sent SUCCESSFULLY!")
    except Exception as e:
        print(f"FAILED to send email: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_email())
