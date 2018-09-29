from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return """Hello Mattie \n\n
I saw you this morning\n
You were moving so fast
Can't seem to loosen my grip
On the past
And I miss you so much
There's no one in sight
And we're still making love
In my secret life
In my secret life""" 

if __name__ == "__main__":
    app.run()
