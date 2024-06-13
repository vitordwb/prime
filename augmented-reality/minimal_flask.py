from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('Ar_js.html', name='World')

if __name__ == '__main__':
    app.run(debug=True)

# eof 