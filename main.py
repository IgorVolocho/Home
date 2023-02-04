import json
import raw_data

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primare_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primare_key=True)
    name = db.Column(db.String(100))
    decription = db.Column(db.String(100))
    start_date = db.Column(db.String())
    end_date = db.Column(db.String())
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executer_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "decription": self.decription,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executer_id": self.executer_id
        }


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201


@app.route("users/<int::uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "User updated", 204

    if request.method == "DELETE":
        u = User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "User delete", 204


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for u in orders.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = User(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )

        db.session.add(new_order)
        db.session.commit()

        return "Order created", 201


@app.route("/orders/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def order(oid: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = Order.query.get(oid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        u = Order.query.get(oid)
        u.name = order_data["order_data"]
        u.description = order_data["order_data"]
        u.start_date = order_data["order_data"]
        u.end_date = order_data["order_data"]
        u.address = order_data["order_data"]
        u.price = order_data["order_data"]
        u.customer_id = order_data["order_data"]
        u.executor_id = order_data["order_data"]

        db.session.add(u)
        db.session.commit()
        return "", 204


@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res = []
        for u in Offer.query.all():
            res.append(u.to_dict())
        return json.dumps(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )
        db.session.add(new_offer)
        db.session.commit()
        return "", 201


@app.route("/offers/<int:oid>", methods=['GET', 'PUT', 'DELETE'])
def offer(oid: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = Offer.query.get(oid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        u = Offer.query.get(oid)
        u.order_id = order_data["order_id"]
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()
        return "", 204


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primare_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age
        }


# init DB
def init_database():
    db.drop_all()
    db.create_all()

    for user_data in raw_data.users:
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )

        db.session.add(new_user)
        db.session.commit()

    for order_data in raw_data.orders:
        new_order = User(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )

        db.session.add(new_order)
        db.session.commit()

    for offer_data in raw_data.offers:
        new_offer = Offer(
            id=offer_data["id"],
            order=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )

        db.session.add(new_offer)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
