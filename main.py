from flask import Flask, request, jsonify
from tinydb import TinyDB
import re

app = Flask(__name__)
db = TinyDB('db.json')
db_table = db.table('forms')


def validate_field_type_by_value(value: str) -> str:

    if re.match(r'^\d{2}\.\d{2}\.\d{4}$', value) or re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return 'date'
    elif re.match(r'^\+7[0-9]{10}$', value):
        return 'phone'
    elif re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value):
        return 'email'
    else:
        return 'text'


def search_form(request_data):
    forms = db_table.all()

    for form in forms:
        if set(form['fields'].items()).issubset(set(request_data.items())):
            return jsonify(form['name'])


@app.route('/get_form', methods=['POST'])
def get_form():

    request_data = {
        key: validate_field_type_by_value(value) for key, value in request.form.to_dict().items()
    }
    form = search_form(request_data)

    return form if form else jsonify(request_data)


if __name__ == '__main__':
    app.run(debug=True)
