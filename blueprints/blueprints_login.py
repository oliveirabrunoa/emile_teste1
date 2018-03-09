import importlib


class BlueprintsLogin:

    def blueprints(self):
        blueprints = []

        blueprint = getattr(importlib.import_module('login'), 'login')
        blueprints.append(blueprint)

        return blueprints
