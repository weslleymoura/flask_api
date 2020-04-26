from flask import jsonify, abort

class RegressionModelOLX():

    def __init__(self, request):
        self.request = request

        # Receive self.request's data
        self.trade_price_last1 = self.request.data.get('trade_price_last1', None)
        self.curve_based_price = self.request.data.get('curve_based_price', None)
        self.curve_based_price_last1 = self.request.data.get('curve_based_price_last1', None)
        self.is_callable = self.request.data.get('is_callable', None)
        self.bond_id = self.request.data.get('bond_id', None)
        self.via_tela = self.request.data.get('via_tela', None)

    def transform(self, model):

        if not self.trade_price_last1:
            response = jsonify({'status_message': 'Did not find value of trade_price_last1'})
            response.status_code = 404
            return response

        if not self.curve_based_price:
            response = jsonify({'status_message': 'Did not find value of curve_based_price'})
            response.status_code = 404
            return response

        if not self.curve_based_price_last1:
            response = jsonify({'status_message': 'Did not find value of curve_based_price_last1'})
            response.status_code = 404
            return response

        if not self.is_callable:
            response = jsonify({'status_message': 'Did not find value of is_callable'})
            response.status_code = 404
            return response

        if not self.bond_id:
            response = jsonify({'status_message': 'Did not find value of bond_id'})
            response.status_code = 404
            return response

        # Convert data types
        self.trade_price_last1 = float(self.trade_price_last1)
        self.curve_based_price = float(self.curve_based_price)
        self.curve_based_price_last1 = float(self.curve_based_price_last1)
        self.is_callable = float(self.is_callable)
        self.bond_id = str(self.bond_id)

        # Compute one hot encoded features
        is_348003 = 0.0
        if self.bond_id == '348003':
            is_348003 = 1.0

        is_195002 = 0.0
        if self.bond_id == '195002':
            is_195002 = 1.0

        # Prepare input data
        input_data = [[self.trade_price_last1, self.curve_based_price, self.curve_based_price_last1, self.is_callable, is_348003, is_195002]]

        # Make predictions
        pred = model.predict(input_data)

        if self.via_tela:
            return '''<h1> Prediction result is {}</h1><br>'''.format(pred[0])

        res = {
            'prediction': pred[0]
            }

        response = jsonify(res)
        response.status_code = 200
        return response
