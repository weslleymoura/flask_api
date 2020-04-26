from flask_api import FlaskAPI
from flask import request
from instance.config import app_config
import logging
from pickle import load
from flask_cors import CORS

def create_app(config_name):

    from app.logic.model import RegressionModelOLX

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # load the model from disk
    model = load(open('/tmp/model.sav', 'rb'))

    CORS(app)

    @app.before_first_request
    def initialization_logic():

        # Create logger (if not app.debug:)
        gunicorn_logger = logging.getLogger('gunicorn.error')
        for handler in gunicorn_logger.handlers:
            app.logger.addHandler(handler)
        app.logger.setLevel(gunicorn_logger.level)

        # How to write in the log file
        app.logger.debug('this is a DEBUG message')
        app.logger.info('this is an INFO message')
        app.logger.warning('this is a WARNING message')
        app.logger.error('this is an ERROR message')
        app.logger.critical('this is a CRITICAL message')

    @app.route('/prediction/', methods=['GET', 'POST'])
    def make_prediction (**kwargs):

        if request.method == 'POST':
            logic = RegressionModelOLX(request=request)
            return logic.transform(model)

        return '''<form method="post">
                Inform input values: <br>
              trade_price_last1: <input type="text" name="trade_price_last1" value="129.08900"/><br>
              curve_based_price: <input type="text" name="curve_based_price" value="127.561201"/><br>
              curve_based_price_last1: <input type="text" name="curve_based_price_last1" value="129.435587"/><br>
              is_callable: <input type="text" name="is_callable" value="0"/><br>
              bond_id: <input type="text" name="bond_id" value="123456"/><br>
              <input type="hidden" name="via_tela" value="1"/><br>

              <p> </p>
              <input type="submit" value="Submit"><br>
              </form>'''

    return app
