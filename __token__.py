def token():
    from urllib.parse import urlencode
    APP_ID = 7056106
    AUTH_URL = 'https://oauth.vk.com/authorize'
    AUTH_DATA = {'client_id': APP_ID, 'display': 'page', 'scope': 'friends', 'response_type': 'token'}
    print('?'.join((AUTH_URL, urlencode(AUTH_DATA))))

if __name__ == "__main__":
    token()