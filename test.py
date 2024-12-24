import smtplib
from email.mime.text import MIMEText
from jinja2 import Template
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#pwd_context.hash()

# password = pwd_context.hash('master123')
# print(password)
print(pwd_context.verify('master123', '$2b$12$mlEbpgOG1UksunxnnaOk3exnsUWnhkGlzXZEYTKqb9eudeLD891s2'))


template = """
<html>
<body>
    <header>This is header</header>
    <h1>Hello {{ name }}!</h1>
    <h3 style="letter-spacing: 5px; font-weight: bold">837894</h3>
    <p>This is a test email with dynamic content.</p>
    <footer>This is footer</footer>
</body>
</html>
"""

"""
html_content = Template(template).render(name="Shiva")


message = MIMEText(html_content, "html")
message["From"] = "shiva@fininfocom.com"
message["To"] = "shivashivam17@gmail.com"
message["Subject"] = "Dynamic HTML Email"


with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("shiva@fininfocom.com", "wutb zjtz bfct ethg")
    server.sendmail("shiva@fininfocom.com", "shivashivam17@gmail.com", message.as_string())
    print("Email sent successfully!")

"""
