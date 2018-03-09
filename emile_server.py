from flask import Flask
import backend
import os
import importlib
import string


def create_app():
    app = Flask("emile")

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    backend.db.init_app(app)
    return app


def register_blueprints(app):
    for module in os.listdir(os.getcwd() + '/blueprints/'):
        if 'blueprints' in module:
            module_name = module.replace('.py', '')
            class_name = string.capwords(module_name.replace('_', ' ')).replace(' ', '')
            cls = getattr(importlib.import_module('blueprints.{0}'.format(module_name)), class_name)
            blueprints =  cls().blueprints()

            for blueprint in blueprints:
                app.register_blueprint(blueprint)



app = create_app()
register_blueprints(app)


if __name__ == '__main__':
    app.run()
