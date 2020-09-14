"""import Flask things and sqlite3."""
from flask import Flask, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import randint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#TODO: Find a way to create separate Product module

#Create db model class Product
class Product(db.Model):
    """Define product class."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, primary_key=False)
    description = db.Column(db.String(200), nullable=False)
    media = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Product %r>' % self.id


@app.route('/')
def homepage():
    """Display homepage."""
    return render_template('home.html')


@app.route('/paintings')
def shop_paintings():
    """Render template for paintings page."""
    return render_template('paintings.html')


@app.route('/about')
def about():
    """Display about page."""
    return render_template('about.html')

# @app.route('/cart')
# def checkout():
#     """Defines checkout functionality"""
#     pass


@app.route('/contact')
def contact_me():
    """Provides contact form for user"""
    return render_template('contact.html')


@app.route('/contact_results')
def contact_results():
    """Redirects user to submission confirmation."""
    return render_template('contact_results.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin page where items can be added to db."""
    return render_template('admin.html')


@app.route('/product_confirmation', methods=['GET', 'POST'])
def confirmation():
    """Confirmation of product addition."""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        media = request.form['media']
        size = request.form['size']
        new_product = Product(title=title,
                              description=description,
                              price=price,
                              media=media,
                              size=size
                              )
        try:
            db.session.add(new_product)
            db.session.commit()
            return render_template('product_confirmation.html')
        except:
            return "There was an issue."
    else:
        products = Product.query.order_by(Product.date_created).all()
        return render_template('admin.html', products=products)


@app.teardown_appcontext
def close_connection(exception):
    """Close our connection to database.db."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
