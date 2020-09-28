"""Import app from online_store package."""
from online_store import app


########################################################################
#                   #TODO:                                             #
########################################################################

# Cart route, checkout
# Contact route to actually submit to something
# Delete profile functionality
# Look into "remember me" and "url_is_safe" functionality for UX/security
# Potentially improve redirect on 404 page to be server-side or JS
# Design custom icon to display when logged in, nav link title for when not ?
# Button in user route not working now for some reason, figure out why
# Clean up styling (checkboxes, links in sign up/login forms, buttons, etc.)

########################################################################
#                   #Run                                               #
########################################################################


if __name__ == "__main__":
    app.run(debug=True)
