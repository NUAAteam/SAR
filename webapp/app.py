from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure

app = Flask(__name__)

@app.route('/')
def home():
    plot = figure()
    # Add your plot code here
    script, div = components(plot)
    return render_template('plot.html', script=script, div=div)

if __name__ == '__main__':
    app.run(debug=True)
