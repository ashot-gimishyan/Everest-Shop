from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


# create and configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# associates an SQLAlchemy instance with a Flask application
db = SQLAlchemy(app)


# The baseclass for all our models is called db.Model.
# It’s stored on the SQLAlchemy instance we have to create.
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isAvailable = db.Column(db.Boolean, default=True)

#    def __repr__(self):
#        return self.name


@app.route('/')
def main():
    items = Item.query.order_by(Item.id).all()
    return render_template('main.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": int(item.price) * 100
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']

        item = Item(name=name, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('add.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == "__main__":
    app.run(debug=True)