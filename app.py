from dotenv import load_dotenv

load_dotenv() 


from flask import Flask, request, jsonify
from mongoengine import connect, Document, StringField, ReferenceField
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
connect( host=os.environ.get("MONGODB"))

SECRET_KEY = os.environ.get("SECRET")

class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

class Template(Document):
    user_id = ReferenceField(User)
    template_name = StringField(required=True)
    subject = StringField(required=True)
    body = StringField(required=True)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=hashed_password).save()
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({'user_id': str(user.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

class TemplateAPI(Resource):

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return User.objects(id=data['user_id']).first()
        except:
            return None

    def post(self):
        token = request.headers.get('Authorization').split(" ")[1]
        user = self.verify_token(token)
        if user:
            data = request.get_json()
            new_template = Template(user_id=user, template_name=data['template_name'], subject=data['subject'], body=data['body']).save()
            return jsonify({'template_id': str(new_template.id), 'message': 'Template created!'})
        return jsonify({'message': 'Invalid token'}), 401

    def get(self, template_id=None):
        token = request.headers.get('Authorization').split(" ")[1]
        user = self.verify_token(token)
        if user:
            if template_id:
                template = Template.objects(id=template_id, user_id=user).first()
                if template:
                    return jsonify({'template': {'template_name': template.template_name, 'subject': template.subject, 'body': template.body}})
                return jsonify({'message': 'No template found'}), 404
            else:
                templates = Template.objects(user_id=user)
                return jsonify({'templates': [{'id':str(t.id),'template_name': t.template_name, 'subject': t.subject, 'body': t.body} for t in templates]})
        return jsonify({'message': 'Invalid token'}), 401

    def put(self, template_id):
        token = request.headers.get('Authorization').split(" ")[1]
        user = self.verify_token(token)
        if user:
            data = request.get_json()
            template = Template.objects(id=template_id, user_id=user).first()
            if template:
                template.update(set__template_name=data['template_name'], set__subject=data['subject'], set__body=data['body'])
                return jsonify({'message': 'Template updated successfully!'})
            return jsonify({'message': 'No template found'}), 404
        return jsonify({'message': 'Invalid token'}), 401

    def delete(self, template_id):
        token = request.headers.get('Authorization').split(" ")[1]
        user = self.verify_token(token)
        if user:
            template = Template.objects(id=template_id, user_id=user).first()
            if template:
                template.delete()
                return jsonify({'message': 'Template deleted successfully!'})
            return jsonify({'message': 'No template found'}), 404
        return jsonify({'message': 'Invalid token'}), 401

api.add_resource(TemplateAPI, '/template', '/template/<string:template_id>')

if __name__ == '__main__':
    app.run(debug=True)

# for prod
# waitress-serve --host 0.0.0.0 app:app
