#!/usr/bin/env python3

import connexion

from eark_ip_rest import encoder
from eark_ip_rest.controllers.static import home, result

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024
    app.app.add_url_rule('/', view_func=home)
    app.app.add_url_rule('/result', methods=['POST'], view_func=result)
    app.add_api('swagger.yaml', arguments={'title': 'E-ARK IP Validation API'}, pythonic_params=True)
    app.run(port=8080)

if __name__ == '__main__':
    main()
