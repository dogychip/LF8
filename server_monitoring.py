import psutil
import smtplib
from email.mime.text import MIMEText
import time

# Konfiguration der Grenzwerte
CPU_THRESHOLD = 80  # in Prozent
MEMORY_THRESHOLD = 80  # in Prozent
DISK_THRESHOLD = 90  # in Prozent
PROCESS_COUNT_THRESHOLD = 300  # Maximale Anzahl an Prozessen

# E-Mail Konfiguration
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_SENDER = "alert@example.com"
EMAIL_RECEIVER = "admin@example.com"
EMAIL_PASSWORD = "yourpassword"

def send_alert(subject, message):
    """Sendet eine Alarm-E-Mail."""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("Alarm-E-Mail gesendet.")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")

def check_system():
    """Überprüft die Systemparameter und sendet bei Bedarf eine Alarmmeldung."""
    alerts = []
    
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        alerts.append(f"Hohe CPU-Auslastung: {cpu_usage}%")
    
    memory_usage = psutil.virtual_memory().percent
    if memory_usage > MEMORY_THRESHOLD:
        alerts.append(f"Hohe RAM-Auslastung: {memory_usage}%")
    
    disk_usage = psutil.disk_usage('/').percent
    if disk_usage > DISK_THRESHOLD:
        alerts.append(f"Wenig Speicherplatz: {disk_usage}% belegt")
    
    process_count = len(psutil.pids())
    if process_count > PROCESS_COUNT_THRESHOLD:
        alerts.append(f"Hohe Prozessanzahl: {process_count} Prozesse")
    
    if alerts:
        alert_message = "\n".join(alerts)
        send_alert("Server-Überlastungsalarm", alert_message)
    else:
        print("Systemstatus: OK")

if __name__ == "__main__":
    while True:
        check_system()
        time.sleep(60)  # Überprüfung alle 60 Sekunden
