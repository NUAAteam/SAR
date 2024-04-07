from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
  slider_value = request.form.get('slider') if request.method == 'POST' else 50
  return render_template('home.html',slider_value=slider_value)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)