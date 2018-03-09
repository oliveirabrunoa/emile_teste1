from flask import Blueprint, jsonify, request
from . import models
from backend import db


institution = Blueprint("institution", __name__)


@institution.route('/institution_details/<institution_id>', methods=['GET'])
def institution_details(institution_id):
    return jsonify(institution=[dict(id=institution.id, name=institution.name,
                                     abbreviation= institution.abbreviation,
                                     cnpj=institution.cnpj, address= institution.address,
                                     current_program_section = institution.current_program_section,
                                     programs=str(institution.programs))
                                for institution in models.Institution.query.filter_by(id=institution_id).all()])
