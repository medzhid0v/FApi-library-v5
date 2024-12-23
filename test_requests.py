import requests

book_template = {'title': 'тестовый', 'author': 'Мага'}
reader_template = {'name': 'тестовый'}
issue_template = {'book_id': 3, 'reader_id': 1}

method = 'issue'

# host = f'http://127.0.0.1:8080/{method}/'
# print(requests.post(host, json=issue_template).json())
#
# host = f'http://127.0.0.1:8080/{method}/'
# print('All - ', requests.get(host).json())
#
# host = f'http://127.0.0.1:8080/{method}/1'
# print('ID - ', requests.get(host).json())

# host = f'http://127.0.0.1:8080/{method}/1'
# print(requests.delete(host).json())
