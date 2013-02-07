from flask import Flask, render_template
import pyplinkseq

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
  vars = pyplinkseq.var_fetch("file=jeff", 10)
  return render_template('index.html', vars=vars)


if __name__ == '__main__':
  pyplinkseq.set_project("/Users/hammer/Dropbox/codebox/personal-genome-analysis/personal-genome-analysis-skillshare.pseq")
  app.run()
