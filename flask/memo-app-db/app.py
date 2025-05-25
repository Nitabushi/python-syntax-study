from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirm', methods=['POST'])
def submit():
    message = request.form['message']
    return render_template('confirm.html',message=message)

@app.route('/complete', methods=['POST'])
def complete():
    message = request.form['message']
    file_path = "data/output.txt"
    with open(file_path, "w", encoding="utf-8")as file:
        file.write(message)
    return render_template('complete.html', message=message, save_path=file_path)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
