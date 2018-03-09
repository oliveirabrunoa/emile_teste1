from backend import db


class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    abbreviation =  db.Column(db.String(20))
    cnpj = db.Column(db.String(18), unique=True)
    address = db.Column(db.String(250))
    current_program_section = db.Column(db.String(6))
    programs = db.relationship('Program', backref='institution', lazy='dynamic')


    def set_fields(self, fields):
        self.name = fields['name']
        self.abbreviation = fields['abbreviation']
        self.cnpj = fields['cnpj']
        self.address = fields['address']
        self.current_program_section = fields['current_program_section']
