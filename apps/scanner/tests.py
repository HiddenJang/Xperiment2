import json
data = {'leon': {'login': 'aaa', 'password': 'bbb'}, 'olimp': {'login': 'ccc', 'password': 'ddd'}}
d = str(data)
d = json.loads(d.replace("'", '"'))
print(type(d))