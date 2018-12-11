from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def getvalue():
    transporterid = request.form['transporterid']
    origin = request.form['origin']
    destination = request.form['destination']
    # print(name) will display name in the terminal
    return render_template('testingGMdirectionServWithAPI.html', id=transporterid, o=origin, d=destination)


if __name__ == '__main__':
    app.run(debug=True)
