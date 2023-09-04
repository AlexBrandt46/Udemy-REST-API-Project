"""
This file just contains the blocklist of the JWT tokens. It will be imported by app and
the logout resource so that tokens can be added to the blocklist when the user logs out
"""

# Normally would use a DB since resetting the app will clear out this set
# and previously revoked JWTs would be valid again
BLOCKLIST = set()
