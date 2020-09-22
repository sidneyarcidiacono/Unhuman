"""import Flask things and sqlite3."""
import os
from imghdr import what
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_PATH'] = 'static/assets'
db = SQLAlchemy(app)


########################################################################
#                   #TODO:                                             #
########################################################################

# Delete product functionality in Admin
# Fix modal styling, other various styling
# Add illustrations/prints page
# Cart route, checkout
# User authentication
# User profiles


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

    def __repr__(self):
        """Specify return val when printing Product."""
        return '<Product %r>' % self.id


########################################################################
#                   #Helper Functions                                  #
########################################################################


def validate_image(stream):
    """Validate images to jpg."""
    header = stream.read(512)
    stream.seek(0)
    img_format = what(None, header)
    if not img_format:
        return None
    print("VALIDATE_IMAGE")
    return '.' + (img_format if img_format != 'jpeg' else 'jpg')


########################################################################
#                   #Routes                                            #
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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin page where items can be added to db."""
    if request.method == 'POST':
        print('Posting from admin')
    elif request.method == 'GET':
        print('getting from admin')
    return render_template('admin.html')


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
            print(request.files['image'])
            uploaded_file = request.files['image']
            filename = secure_filename(uploaded_file.filename)
            if filename:
                file_ext = os.path.splitext(filename)[1]
                if file_ext != validate_image(uploaded_file.stream):
                    return "Invalid image", 400
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
                    return redirect(url_for('shop_paintings'))
                except ValueError:
                    return render_template('admin.html')
        except:
            return redirect(url_for('admin'))
        # finally:
        #     print("In finally")
        #     return render_template('admin.html')
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
