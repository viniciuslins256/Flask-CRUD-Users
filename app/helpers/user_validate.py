import re


class UserValidate():

    def __init__(self, data):
        self.validate_cpf(data.get("cpf"))
        self.validate_email(data.get("email"))
        self.validate_pis(data.get("pis"))
        self.validate_postal_code(data.get("postal_code"))

    def validate_cpf(self, cpf):
        if not cpf.isdigit():
            raise ValueError("CPF must be digit only")
        if not len(cpf)==11:
            raise ValueError("CPF must have 11 digits")

    def validate_email(self, email):
        validation = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if not re.search(validation, email):   
            raise ValueError("Email must be digit only")
    
    def validate_pis(self, pis):
        if not pis.isdigit():
            raise ValueError("PIS must be digit only")
        if not len(pis)==11:
            raise ValueError("PIS must have 11 digits")

    def validate_postal_code(self, postal_code):
        if not postal_code.isdigit():
            ValueError("Postal Code must be number only")
        if len(postal_code) not in range(7, 10):
            ValueError("Postal Code must have 7, 8 or 9 digits only")
    