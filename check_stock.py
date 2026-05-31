import os
import sys
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STORE_ID = "101"

PRODUCTS = {
    'MacBook Pro 14"': "https://www.microcenter.com/product/709137/apple-macbook-pro-nano-texture-14-z1ml002hc-(early-2026)-142-laptop-computer-space-black?sp=343",
    'MacBook Pro 16"': "https://www.microcenter.com/product/708934/apple-macbook-pro-nano-texture-16-z1mz001aj-(early-2026)-162-laptop-computer-space-black?sp=587",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_stock(url):
    session = requests.Session()
    session.cookies.set("storeSelected", STORE_ID, domain=".microcenter.com")
    response = session.get(url, headers=HEADERS, timeout=15)
    return "'inStock':'True'" in response.text

def send_email(product_name, url):
    email_user = os.environ["EMAIL"]
    email_password = os.environ["PASSWORD"]

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user
    msg['Subject'] = f'{product_name} is Now In Stock!'
    msg.attach(MIMEText(
        f'{product_name} is now in stock.\n\n{url}\n\nGet it before it sells out!',
        'plain'
    ))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_user, msg.as_string())

    print(f"Alert sent for {product_name}!")

test_mode = os.environ.get("TEST_EMAIL", "false").lower() == "true"

any_error = False
for name, url in PRODUCTS.items():
    try:
        if test_mode or check_stock(url):
            print(f"IN STOCK: {name}" if not test_mode else f"TEST: {name}")
            send_email(name, url)
        else:
            print(f"Out of stock: {name}")
    except Exception as e:
        print(f"Error checking {name}: {e}")
        any_error = True

if any_error:
    sys.exit(1)
