import requests
from bs4 import BeautifulSoup as bs4

def getBalance(cardNumber):
    """
    Return the balance of card
    """

    url = "https://epay.transcard.kz/card-info"

    session = requests.Session()

    r = session.get(url)
    html_bytes = r.text
    soup = bs4(html_bytes, 'lxml')
    token = soup.find('input', {'name':'_token'})['value']

    data = {
        'cardNumber': cardNumber,
        '_token': token,
    }


    r = session.post(url, data=data)
    html_bytes = r.text
    soup = bs4(html_bytes, 'lxml')
    try:
        cardNumber = soup.find('input', {'name':'CardNumber'})['value']
        cardBalance = int(float(soup.find("span", style="color: #d23c3c;").text))
    except:
        raise ValueError('Invalid card number')
    
    return cardBalance

if __name__== "__main__":
    print(getBalance(1001564614))

