from crypt import methods
from datetime import datetime 
from locale import format_string
from unicodedata import name
from urllib.request import url2pathname
from flask import Flask, jsonify, redirect, render_template, request, session, url_for, abort
from sqlalchemy import cast, String
from flask_sqlalchemy import SQLAlchemy
from mysqlx import Session
from flask_session import Session
from html5lib import serialize
from itsdangerous import Serializer
from marshmallow import Schema, fields
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import and_, desc,asc
from flask_migrate import Migrate
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
import threading
import json
import requests
import time

app = Flask(__name__)

# database user:password@hostname/database name

app.config["SESSION_PERMANENT"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://james:foxtrot09er@localhost/penzi_final'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes = 30)
app.config["SECRET_KEY"] = 'jisungparkfromdeep'
app.config["SESSION_TYPE"] = 'sqlalchemy'


db = SQLAlchemy(app)
admin = Admin(app, name="Admin Portal", template_mode="bootstrap3")


app.config["SESSION_TYPE"] = db
sess = Session()


migrate = Migrate(app, db)


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        
        else:
            abort(403)

class NotificationsViews(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/notify.html")

class LogoutViews(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/logout.html")

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.String(13), unique = True, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    county = db.Column(db.String(60), nullable=False)
    town = db.Column(db.String(60), nullable=False)
    education_level = db.Column(db.String(50), nullable=True)
    profession = db.Column(db.String(60), nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    religion = db.Column(db.String(50), nullable=True)
    tribe = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    matched_by = db.Column(db.String(13), nullable = True)
    time_of_registry = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())


    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_age(cls, age):
        return cls.query.filter_by(age=age).first()

    @classmethod
    def get_by_number(cls, number):
        return cls.query.filter_by(number=number).first()
        

    @classmethod
    def filter_by_age(cls, age, county):
        return cls.query.filter_by()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer()
    gender = fields.String()
    county = fields.String()
    town = fields.String()
    education_level = fields.String()
    profession = fields.String()
    marital_status = fields.String()
    religion = fields.String()
    tribe = fields.String()
    description = fields.String()
    number = fields.Integer()
    status = fields.String()
    matched_by = fields.String()
    time_of_registry = fields.DateTime()


class Incoming_Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_number = db.Column(db.String(13), nullable=False)
    message = db.Column(db.String(160), nullable=True)
    shortcode = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(20), nullable = True)
    delivery_time = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())
   

    def __repr__(self):
        return self.sender_number

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_sender_number(cls, sender_number):
        return cls.query.order_by(asc(sender_number=sender_number)).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Incoming_MessageSchema(Schema):
    id = fields.Integer()
    sender_number = fields.String()
    message = fields.String()
    shortcode = fields.Integer()
    status = fields.String()
    delivery_time = fields.DateTime()



class Outgoing_Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender_number = db.Column(db.String(13), nullable=False)
    message = db.Column(db.String(160), nullable = True)
    shortcode = db.Column(db.Integer(), nullable=False)
    delivery_time = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())
   

    def __repr__(self):
        return self.sender_number

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_sender_number(cls, sender_number):
        return cls.query.order_by(asc(sender_number=sender_number)).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

 
class Outgoing_MessageSchema(Schema):
    id = fields.Integer()
    sender_number = fields.String()
    message = fields.String()
    # message_details = fields.String()
    # message_myself = fields.String()
    # message_match = fields.String()
    shortcode = fields.Integer()
    delivery_time = fields.DateTime()



class Penzi(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    shortcode = db.Column(db.Integer(), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True),
                         nullable=False, server_default=func.now())

    def __repr__(self):
        return self.shortcode

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PenziSchema(Schema):
    id = fields.Integer()
    message = fields.String()
    shortcode = fields.Integer()
    datetime = fields.DateTime()


admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Incoming_Message, db.session))
admin.add_view(SecureModelView(Outgoing_Message, db.session))
admin.add_view(NotificationsViews(name='Notifications', endpoint='notify'))
admin.add_view(LogoutViews(name='Logout', endpoint='logout'))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email") == "james@admin.com" and request.form.get("password") == "admin":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            return render_template("login.html", failed = True)
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
   
    

@app.route("/get_incoming_messages", methods=["GET"])
def get_all_users():

    recipes = Incoming_Message.get_all()
    serializer = UserSchema(many=True)
    data = serializer.dump(recipes)

    return jsonify(
        data
    )


@app.route("/post_incoming_messages", methods=["POST"])
def incoming_messages_post():
    message_data = request.get_json()

    

    message_m = Incoming_Message(

        
        sender_number=message_data.get("sender_number"),
        message=message_data.get("message"),
        shortcode=message_data.get("shortcode"),
        status = "unprocessed"

    )

    message_m.save()
    serializer = Incoming_MessageSchema()
    message_data = serializer.dump(message_m)

    return jsonify(message_data), 201
 

@app.route("/fetch_incoming_messages", methods = ["GET"])
def fetch_incoming_messages():
    message_data = Incoming_Message.query.filter(Incoming_Message.status == "unprocessed").order_by(Incoming_Message.id.desc()).first()
    serializer = Incoming_MessageSchema()
    data = serializer.dump(message_data)

    return data.get("message")


@app.route("/fetch_incoming_messages_sender", methods = ["GET"])
def fetch_incoming_messages_sender():
    message_data = Incoming_Message.query.filter(Incoming_Message.status == "unprocessed").order_by(Incoming_Message.id.desc()).first()
    serializer = Incoming_MessageSchema()
    data = serializer.dump(message_data)
    
    return data.get("sender_number")


@app.route("/get_penzi_message/<int:id>", methods=["GET"])
def get_penzi_message(id):
    message_id = Penzi.get_by_id(id)
    Serializer = PenziSchema()
    data = Serializer.dump(message_id)

    return data.get("message"), 200

@app.route("/update_status/<string:number>", methods = ["PUT"])
def update_status(number):
    status_to_update = Incoming_Message.query.filter(Incoming_Message.sender_number == number).order_by(Incoming_Message.id.desc()).first()
    data = request.get_json()
    status_to_update.status = data.get("status")

    db.session.commit()
    serializer = Incoming_MessageSchema()
    status_data = serializer.dump(status_to_update)

    return jsonify(status_data),201


@app.route("/post_outgoing_message", methods=["POST"])
def post_outgoing_message():
    message_data = request.get_json()

    message_m = Outgoing_Message(


        sender_number = message_data.get("sender_number"),
        message = message_data.get("message"),
        shortcode = message_data.get("shortcode")

    )

    message_m.save()
    serializer = Outgoing_MessageSchema()
    message_data = serializer.dump(message_m)
    return jsonify(message_data), 201



@app.route("/get_outgoing_message/<string:sender_number>", methods=["GET"])
def get_message_start(sender_number):
    serial_query = Outgoing_Message.query.filter(Outgoing_Message.sender_number.like(''+sender_number+'')).order_by(Outgoing_Message.id.desc()).first()
    Serializer = Outgoing_MessageSchema()
    data = Serializer.dump(serial_query)

    return data.get("message"), 200


@app.route("/post_start_message_to_user", methods=["POST"])
def post_start_message_to_user():
    user_data = request.get_json()
    user_m = User(


        name=user_data.get("name"),
        age=user_data.get("age"),
        gender=user_data.get("gender"),
        county=user_data.get("county"),
        town=user_data.get("town"),
        number=user_data.get("number")

    )

    user_m.save()
    serializer = UserSchema()
    user_data = serializer.dump(user_m)
    return jsonify(user_data), 201



@app.route("/update_user_details/<string:number>", methods=["PUT"])
def update_user_details(number):
    user_to_update = User.get_by_number(number)

    data = request.get_json()

    user_to_update.education_level = data.get("education_level")
    user_to_update.profession = data.get("profession")
    user_to_update.marital_status = data.get("marital_status")
    user_to_update.religion = data.get("religion")
    user_to_update.tribe = data.get("tribe")

    db.session.commit()

    serializer = UserSchema()

    data = serializer.dump(user_to_update)

    return jsonify(data), 200



@app.route("/update_user_myself/<string:number>", methods=["PUT"])
def update_user_myself(number):
    user_to_update = User.get_by_number(number)

    data = request.get_json()

    user_to_update.description = data.get("description")

    db.session.commit()

    Serializer = UserSchema()

    recipe_data = Serializer.dump(user_to_update)

    return jsonify(recipe_data), 200




@app.route("/update_status_user/<string:number>", methods = ["PUT"])
def update_status_user(number):
    status_to_update = User.query.filter(User.number == number).first()
    data = request.get_json()
    status_to_update.status = data.get("status")

    db.session.commit()
    serializer = UserSchema()
    status_data = serializer.dump(status_to_update)

    return jsonify(status_data),201



@app.route("/get_gender/<string:number>", methods=["GET"])
def get_age(number):
    serial_query = User.get_by_number(number)
    Serializer = UserSchema()
    data = Serializer.dump(serial_query)

    return data.get("gender"), 200



@app.route("/search_number_of_genders_matched/<int:age1>/<int:age2>/<string:county>/<string:gender>", methods=["GET"])
def search_number_of_genders_matched(age1, age2, county, gender):
    data = User.query.filter(and_(User.age >= age1), (User.age) <= age2, (User.county.like(
        '%'+county+'%')), (User.gender.like(''+gender+''))).count()

    return str(data)



@app.route("/search_query/<int:age1>/<int:age2>/<string:county>/<string:gender>", methods=["GET"])
def search_query(age1, age2, county, gender):
    data = User.query.filter(and_(User.age >= age1), (User.age) <= age2, (User.county.like(
        '%'+county+'%')), (User.gender.like(''+gender+'')))
    serializer = UserSchema(many=True)
    data = serializer.dump(data)

    return jsonify(data), 200



@app.route("/describe_by_number/<string:number>", methods=["GET"])
def describe_by_number(number):
    query = User.get_by_number(number)
    serializer = UserSchema()
    data = serializer.dump(query)

    return jsonify(data), 200


@app.route("/matched_by/<string:number>", methods = ["PUT"])
def matched_by(number):
    user_to_update = User.query.filter(User.number == number).first()
    data = request.get_json()
    user_to_update.matched_by = data.get("matched_by")

    db.session.commit()
    serializer = UserSchema()
    data = serializer.dump(user_to_update)

    return jsonify(data), 201


@app.route("/get_notice1_user/<string:number>", methods = ["GET"])
def get_notice1_user(number):
    user_query = User.get_by_number(number)
    serializer = UserSchema()
    data = serializer.dump(user_query)

    return jsonify(data), 200

@app.route("/get_username/<string:number>", methods = ["GET"])
def get_username(number):
    user_query = User.get_by_number(number)
    serializer = UserSchema()
    data = serializer.dump(user_query)

    return data.get("name"), 200

@app.route("/recipe/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe_to_delete = User.get_by_id(id)

    recipe_to_delete.delete()

    return jsonify({"message": "Deleted"}), 204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource not found"}), 404


@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "Problem at local server"}), 500


if __name__ == "__main__":
    db.create_all()
    app.run(port=8010, debug=True)
