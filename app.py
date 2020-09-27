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

########################################################################
#                   #Run                                               #
########################################################################


if __name__ == "__main__":
    app.run(debug=True)
