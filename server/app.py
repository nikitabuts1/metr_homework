from server.backend.calculator import ChiSquaredNormalCheck
from server.backend.forms import Form
from server.backend.reader import reader, ReaderError
from server.dev_settings import settings

import flask
import flask_cors
from werkzeug.utils import secure_filename

from typing import Dict
import os

import numpy as np

env = os.environ.get("APP_ENV", "dev")
print(f"Starting application in {env} mode")

class ChiApp(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flask_cors.CORS(self)

        self.settings: Dict[str, float] = settings

        self.checker = ChiSquaredNormalCheck(
            conf_level=self.settings['conf_level'],
            num_parts=int(self.settings['num_parts'])
        )

        self.route("/")(self.start)
        self.route("/submit", methods=("GET", "POST"))(self.submit)
        self.after_request(self.remove_file)
        self.before_request(self.before_request_func)

    def before_request_func(self):
        flask.session['path'] = 'init'

    def remove_file(self, response):
        try:
            os.remove(flask.session['path'])
        except FileNotFoundError:
            pass
        return response

    def start(self):
        return flask.render_template('start.html')

    def submit(self):
        form = Form()
        if form.validate_on_submit():
            f = form.file.data
            filename = secure_filename(f.filename)
            path = os.path.join(
                self.root_path, filename
            )
            f.save(path)
            flask.session['path'] = path
            try:
                data: np.ndarray = reader(path)
            except ReaderError:
                return flask.jsonify({
                    'Status': 'Error',
                    'Answer': "File reading went wrong, try check your file's data"
                })
            self.checker = ChiSquaredNormalCheck(
                conf_level=float(form.conf_level.data),
                num_parts=int(form.num_parts.data)
            )
            res, h, our_prob, normal_prob, s_sq, X = self.checker.compute(data)
            import json
            return flask.jsonify({
                'Input values': str(
                    ', '.join(
                        list(
                            map(
                                str, data.tolist()
                            )
                        )
                    )
                ),
                'Status': 'OK',
                'Answer': 'Success',
                'Is normal?': 'No' if not res else 'Yes',
                'h': str(h),
                's_sq': str(s_sq),
                'X': str(X),
                'Out probs': str(
                    ', '.join(
                        list(
                            map(
                                str, our_prob.tolist()
                            )
                        )
                    )
                ),
                'Normal probs': str(
                    ', '.join(
                        list(
                            map(
                                str, normal_prob.tolist()
                            )
                        )
                    )
                ),
            })
        return flask.render_template('base.html', form=form)




