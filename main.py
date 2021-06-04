import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

BUY_PRICE = 27999.0

# Your mail and Password
my_email = "YOUR EMAIL"
password = "EMAIL PASSWORD"

# Creating Soup
URL = "https://www.amazon.in/gp/product/B089H13XX8/ref=s9_acss_bw_cg_top_2a1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s" \
      "=merchandised-search-6&pf_rd_r=BMW6C6BY35J7KPF1DKBA&pf_rd_t=101&pf_rd_p=7ad4fa0e-ce94-46f4-9dee-71920b807f2b" \
      "&pf_rd_i=1375458031 "
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.212 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}
response = requests.get(url=URL, headers=header)
soup = BeautifulSoup(response.content, "lxml")
price = soup.find(id="priceblock_ourprice").get_text()

# Getting price from the soup
price_without_currency = price.split()[1].replace(",", "")
price_float = float(price_without_currency)
title = soup.find(id="productTitle").get_text().strip()

# Sending mail if price drops
if price_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        result = connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )
