from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from wtforms.validators import ValidationError
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)


@app.route("/")
def hello():
    time.sleep(5)
    results = []
    with open("results.txt", mode="r") as f:
        for line in f.readlines():
            result = line.replace("\n", "").split("|")
            results.append(result)
        f.close()
    results.reverse()
    headers = ['Text', 'Prediction']
    return render_template("index.html", headers=headers, results=results)


# if __name__ == '__main__':
def app_run():
    app.secret_key = "samodel"
    bootstrap = Bootstrap(app)
    app.run(host="0.0.0.0", port=8062)
    # app.run()
