import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from plyer import notification
from twilio.rest import Client

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="006655@Chitra",
        database="CPUMETRIC"
    )

def get_admin_contacts():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT name, email, phone FROM Admin")
        admins = cur.fetchall()
        cur.close()
        conn.close()
        return admins
    except Exception as e:
        print("Error fetching admin contacts:", e)
        return []

def send_email(to_email, subject, body):
    try:
        sender = "dummy.alerts.system@gmail.com"
        password = "your_app_password_here"
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Failed to send email:", e)

def send_whatsapp_message(to_number, message):
    try:
        account_sid = "ACbea2c717596526efee54fdad2f2cb3ec"
        auth_token = "3a896a1f7ed84e1b7ad1143b964f9793"
        client = Client(account_sid, auth_token)
        from_whatsapp = "whatsapp:+14155238886"
        to_whatsapp = f"whatsapp:+91{to_number}"
        client.messages.create(
            body=message,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        print("WhatsApp sent")
    except Exception as e:
        print("Failed to send WhatsApp:", e)

def show_system_notification(title, message):
    try:
        notification.notify(title=title, message=message, timeout=5)
    except Exception as e:
        print("Popup failed:", e)

def send_alert(system_id, message):
    print("System alert:", message)
    show_system_notification("Alert", message)
    send_admin_notification(message)

def send_admin_notification(message):
    admins = get_admin_contacts()
    for admin in admins:
        if admin["email"]:
            send_email(admin["email"], "System Alert", message)
        if admin["phone"]:
            send_whatsapp_message(admin["phone"], message)
