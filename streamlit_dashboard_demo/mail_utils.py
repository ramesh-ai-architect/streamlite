import smtplib
from email.message import EmailMessage

def send_feedback_email(feedback_text, user="Anonymous"):
    msg = EmailMessage()
    msg.set_content(f"Feedback from {user}:{feedback_text}")
    msg['Subject'] = "📬 New Feedback Submission"
    msg['From'] = "your_email@example.com"
    msg['To'] = "recipient@example.com"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("your_email@example.com", "your_app_password")
            smtp.send_message(msg)
        return True
    except Exception:
        return False