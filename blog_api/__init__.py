import os

from flask import Flask

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog_api.sqlite')
    )

    if config_name == 'production':
        # will set production related configuration here
        print('production')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello_world():
        return 'Hello, world'

    return app

create_app()
