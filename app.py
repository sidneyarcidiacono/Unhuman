"""import Flask things and sqlite3."""
from flask import Flask, request, render_template, g
from sqlite import Database


app = Flask(__name__)

db = Database()

@app.route('/')
def homepage():
    """Display homepage."""
    return render_template('home.html')


@app.route('/paintings')
def shop_paintings():
    """Render template for paintings page."""
    return render_template('paintings.html')

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
    title = request.form.get('title')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    media = request.form.get('media')
    size = request.form.get('size')

    db.insert_product(title, description, price, media, size)

    print(f"title:{title} description:{description} price:{price} media:{media} size:{size}")
    return render_template('product_confirmation.html')


@app.teardown_appcontext
def close_connection(exception):
    """Close our connection to database.db."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)
