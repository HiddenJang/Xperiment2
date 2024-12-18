auth_data = {'login': {'1':'2', '2':'3'}, 'password': ''}
print(auth_data['login'].keys())
if not (auth_data['login'] or auth_data['password']):
    print('empty')