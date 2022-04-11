from requests import get, post, delete

print(get('http://localhost:5000/api/products').json())

print(delete('http://localhost:5000/api/products/6').json())

print(get('http://localhost:5000/api/products').json())