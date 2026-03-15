import os
import asyncio
from dotenv import load_dotenv

async def test():
    # Print the current env var without override
    print("BEFORE load_dotenv():")
    print("User:", os.getenv("MAIL_USERNAME"))
    print("Pass:", os.getenv("MAIL_PASSWORD"))

    # Load with override
    load_dotenv(override=True)
    
    print("AFTER load_dotenv(override=True):")
    print("User:", os.getenv("MAIL_USERNAME"))
    print("Pass:", os.getenv("MAIL_PASSWORD"))

if __name__ == "__main__":
    asyncio.run(test())
