"""Import app from online_store package."""
from online_store import app


########################################################################
#                   #TODO:                                             #
########################################################################

# Enable editing product in admin route.
# Automation email when someone purchases an item (later)
# Look into "url_is_safe" functionality for security
# Potentially improve redirect on 404 page to be server-side or JS
# Design custom icon to display when logged in, nav link title for when not ?
# Custom checkout page with Stripe (future)

# Production todos:
# Blueprints for python files

########################################################################
#                   #Run                                               #
########################################################################


if __name__ == "__main__":
    app.run(debug=True)
