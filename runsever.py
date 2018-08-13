from os import environ
from ung_dung import app
if __name__=="__main__":
    HOST=environ.get("SERVER_HOST","localhost")
    try:
        PORT=int(environ.get("SERVER_POST","1234"))
    except ValueError:
        pass
    app.run(HOST,PORT)
    