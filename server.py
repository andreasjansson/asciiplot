import sys
import os
import tempfile
import numpy as np
from StringIO import StringIO
import pandas as pd
import gnuplotlib as gp
from flask import (
    Flask, request
)

app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET', 'POST'])
def index():
    text_plain = {'Content-type': 'text/plain'}

    piped = request.get_data()
    if piped:
        data = data_from_csv(piped)
    elif 'values' in request.args:
        data = data_from_values(request.args['values'])
    elif 'csv' in request.args:
        data = data_from_csv(request.args['csv'])
    else:
        return usage(), 400, text_plain

    if not np.issubdtype(data.dtype, np.number):
        return usage(), 400, text_plain

    width = int(request.args.get('width', 80))
    height = int(request.args.get('height', 20))

    return plot(data, width, height), 200, text_plain


def data_from_csv(s):
    return pd.read_csv(StringIO(s), header=None).as_matrix()


def data_from_values(s):
    return data_from_csv(s.replace(',', '\n'))  # ugly


def usage():
    return 'Bad usage.\n\nPlease see examples at http://github.com/andreasjansson/asciiplot\n'


def plot(data, width, height):
    times = np.arange(data.shape[0])
    args = [(times, xs, {'with': 'lines'}) for xs in data.T]
    filename = tempfile.NamedTemporaryFile(delete=False).name
    try:
        gp.plot(
            *args,
            _with='lines',
            terminal='dumb %d,%d' % (width, height),
            unset='grid',
            set='tics scale 0',
            output=filename
        )

        with open(filename) as f:
            return f.read()[1:]

    finally:
        os.unlink(filename)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=len(sys.argv) > 1 and sys.argv[1] == 'debug',
        threaded=True,
        port=80
    )
