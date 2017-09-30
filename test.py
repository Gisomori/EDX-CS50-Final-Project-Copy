
Python3 example:

http://pset8.cs50.net/articles?geo=02138

import urllib.request, json
with urllib.request.urlopen("http://pset8.cs50.net/articles?geo=02138") as url:
    data = json.loads(url.read().decode())
    print(data)



    print request.GET['username'] # for GET form method
print request.POST['username'] # for POST form method



@app.route('/_get_current_user')
def get_current_user():
    return jsonify(username=g.user.username,
                   email=g.user.email,
                   id=g.user.id)


{
    "username": "admin",
    "email": "admin@localhost",
    "id": 42
}


jsonify(link = data.)