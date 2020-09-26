"""import Flask things and sqlite3."""
import os
import config
from dotenv import load_dotenv
from imghdr import what
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, g, redirect, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt

app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app)

# Define flask-login config variables & instantiate LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'user'


########################################################################
#                   #TODO:                                             #
########################################################################

# Fix modal styling, other various styling
# Add illustrations/prints page
# Cart route, checkout
# Log out functionality
# User profiles
# Potentially refactor to use WTForms
# Figure out how to better track users with flask_sqlalchemy
# Look into "remember me" and "url_is_safe" functionality for UX/security


########################################################################
#                   #db.Model classes                                  #
########################################################################


class Product(db.Model):
    """Define product class."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, default=1)
    description = db.Column(db.String(200), nullable=False)
    media = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """Specify return val when printing Product."""
        return '<Product %r>' % self.id


class User(UserMixin, db.Model):
    """Define user class."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship("Product", backref='user', lazy=True)

    def is_authenticated(self):
        """Return true when called after verifying login."""
        return True

    def check_password(self, password):
        """Verify hashed password and inputted password."""
        return sha256_crypt.verify(password, self.password)


@login_manager.user_loader
def load_user(id):
    """Define user callback for user_loader function."""
    return User.query.get(id)

########################################################################
#                   #Helper Functions                                  #
########################################################################


def create_user(pass_one, pass_conf, name, email):
    """Return new user from User class."""
    user_password = ''
    if pass_one == pass_conf:
        user_password = sha256_crypt.hash(pass_one)
        new_user = User(name=name,
                        email=email,
                        password=user_password
                        )
        return new_user
    else:
        context = {
            'message': 'Please make sure passwords match.'
        }
        return render_template('user.html', **context)

########################################################################
#                   #Error Handling                                    #
########################################################################

# @app.errorhandler(404)
# def page_not_found(e):
#     print(e)
#     return render_template('404.html')

########################################################################
#                   #Public Routes                                     #
########################################################################


@app.route('/')
def homepage():
    """Display homepage."""
    return render_template('home.html')


@app.route('/paintings')
def shop_paintings():
    """Render template for paintings page."""
    paintings = Product.query.all()
    print(paintings)
    context = {
        'paintings': paintings
    }
    return render_template('paintings.html', **context)


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
    """Provide contact form for user."""
    return render_template('contact.html')


@app.route('/contact_results')
def contact_results():
    """Redirects user to submission confirmation."""
    return render_template('contact_results.html')


########################################################################
#                   #User & Login routes                               #
########################################################################


@app.route('/user', methods=['GET', 'POST'])
def user():
    """Sign up users."""
    if request.method == 'GET':
        return render_template('user.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Sign Up!':
            name = request.form['name']
            email = request.form['email']
            pass_first = request.form['password']
            pass_conf = request.form['password-conf']
            new_user = create_user(pass_first, pass_conf, name, email)
            login_user(new_user)
            new_user.is_authenticated = True
            try:
                db.session.add(new_user)
                db.session.commit()
                context = {
                    'message': f'Thank you for signing up, {name}'
                }
                return render_template('home.html', **context)
            except ValueError:
                context = {
                    'message': 'Something went wrong.'
                }
                return render_template('user.html', **context)
        elif request.form['submit'] == 'Log In':
            try:
                email = request.form['email']
                user = User.query.filter_by(email=email).first()
                entered_pass = request.form['password']
                if user.check_password(entered_pass):
                    user.is_authenticated = True
                    login_user(user, remember=True)
                    db.session.add(user)
                    db.session.commit()
                return redirect(url_for('homepage'))
            except ValueError:
                context = {
                    'message': 'Invalid username or password.'
                }
                return render_template('user.html', **context)
        return "There was a problem"


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('user'))


########################################################################
#                   #Admin Routes                                      #
########################################################################


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """Admin page where items can be added to db."""
    if current_user.is_authenticated:
        print(f"is anonymous?: {current_user.is_anonymous}")
        products = Product.query.order_by(Product.date_created).all()
        context = {
            'products': products
        }
        return render_template('admin.html', **context)
    print(f"Is authenticated? from else {current_user.is_authenticated}")
    return redirect(url_for('user'))


@app.route('/admin-delete/<product_id>')
def delete_product(product_id):
    """Delete products from database."""
    try:
        product_to_delete = Product.query.filter_by(id=product_id).first()
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect(url_for('admin'))
    except(TypeError, ValueError):
        print("Something went wrong deleting this product.")
        return redirect(url_for('admin'))


@app.route('/product_confirmation', methods=['GET', 'POST'])
def confirmation():
    """Confirm of product addition."""
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            media = request.form['media']
            size = request.form['size']
            uploaded_file = request.files['image']
            filename = secure_filename(uploaded_file.filename)
            if filename:
                file_ext = os.path.splitext(filename)[1]
                file_path = os.path.join(
                   app.config['UPLOAD_PATH'], filename
                )
                uploaded_file.save(file_path)
                new_product = Product(title=title,
                                      description=description,
                                      price=price,
                                      media=media,
                                      size=size,
                                      image=file_path)
                try:
                    db.session.add(new_product)
                    db.session.commit()
                    return redirect(url_for('confirmation'))
                except ValueError:
                    return render_template('admin.html')
        except:
            return redirect(url_for('admin'))
    else:
        products = Product.query.order_by(Product.date_created).all()

        context = {
            'products': products
        }
        return render_template('admin.html', **context)


########################################################################
#                   #Teardown & Run                                    #
########################################################################


@app.teardown_appcontext
def close_connection(exception):
    """Close our connection to database.db."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
