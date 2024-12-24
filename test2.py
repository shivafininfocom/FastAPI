import firebase_admin
from firebase_admin import messaging, credentials

# Initialize Firebase Admin SDK
cred = credentials.Certificate("D:/shivat/FastAPI/flutter_notifications.json")
firebase_admin.initialize_app(cred)

# Send notification
message = messaging.Message(
    notification=messaging.Notification(
        title="Hello Users",
        body="This is a notification from the LT metro",
    ),
    topic="all"
)

response = messaging.send(message)
print(f"Successfully sent message: {response}")


