import urllib.request
import json

url = "https://jsonplaceholder.typicode.com/posts/1"

response = urllib.request.urlopen(url)
data = json.loads(response.read())

print("Title:", data["title"])
print("Body:", data["body"])