import os
import importlib
import pdb


class BlueprintsCruds:

    def blueprints(self):
        blueprints = []

        for crud in os.listdir(os.getcwd() + '/cruds/'):
            if 'crud' in crud:
                blueprint = getattr(importlib.import_module('cruds.{0}.services'.format(crud)), crud.replace('crud_', ''))
                blueprints.append(blueprint)

        return blueprints
