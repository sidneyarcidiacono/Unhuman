"""import Flask things and sqlite3."""
from flask import Flask, request, render_template, g
import sqlite3


app = Flask(__name__)


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


@app.teardown_appcontext
def close_connection(exception):
    """Close our connection to database.db."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
