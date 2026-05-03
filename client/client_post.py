import urllib.request
import urllib.parse

url = "http://localhost/cgi-bin/book.py"

data = {
    "name": "Swetha",
    "email": "swetha@gmail.com",
    "date": "2026-05-10",
    "slot": "10AM"
}

encoded_data = urllib.parse.urlencode(data).encode()

request = urllib.request.Request(url, data=encoded_data)
response = urllib.request.urlopen(request)

print(response.read().decode())