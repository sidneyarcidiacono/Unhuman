"""Import app from online_store package."""
from online_store import app


########################################################################
#                   #TODO:                                             #
########################################################################

# Quantity to show in cart
# Fix cart session so that it totals and checks out for all items in cart
# Webhooks
# Automation email when someone purchases an item (later)
# Different pages/sections on products page for different sections (prints, paintings)
# Delete profile functionality
# Look into "url_is_safe" functionality for security
# Potentially improve redirect on 404 page to be server-side or JS
# Design custom icon to display when logged in, nav link title for when not ?
# Clean up styling (checkboxes, links in sign up/login forms, buttons, etc.)
# Switch to POSTGRES or MYSQL
# Add content & go live!!!!

########################################################################
#                   #Run                                               #
########################################################################


if __name__ == "__main__":
    app.run(debug=True)
