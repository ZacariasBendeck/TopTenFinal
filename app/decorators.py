from functools import wraps
from flask import g, flash, redirect, url_for
from flask import session as login_session
import logging

# ' Decorator Login Function
# User Helper Functions


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            flash('You need to be logged in to access this area')
            return redirect('/login')
        else:
            return f(*args,**kwargs)
    return decorated_function

def user_authorized(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		if kwargs['owner_id'] == login_session['user_id']:
			logging.info('User authorized')
			return f(*args, **kwargs)
		else:
			flash('You are not authorized to go there. ')
			logging.warning('A user was denied access to a page!')
			return redirect(url_for('mainPage'))
	return decorated_function
