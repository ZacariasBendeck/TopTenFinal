from flask import Flask, render_template, url_for, request
from flask import redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Owner, Lists, Items

# 'oauth imports
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from datetime import datetime

from flask import g, request

from app.decorators import *




CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Top Ten Lists"

app = Flask(__name__)

engine = create_engine('sqlite:///finalProject.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/topten/')
def mainPage():
    """Returns the home page for Top Ten List App """
    owners = session.query(Owner).all()    
    if (owners != []): section2 = str(ownerListSection(1))
    else: section2 = ''
    return render_template('mainPage.html', items=owners,
                           login_session=login_session, section2=section2)


# ' Start of pages for working with lists ' #
@app.route('/topten/<int:owner_id>/')
def ownerLists(owner_id):
    """ Returns the page of lists for an owner, given owner_id"""
    lists = session.query(Lists).filter_by(owner_id=owner_id).all()
    owner = session.query(Owner).filter_by(id=owner_id).one()
    return render_template('ownerLists.html', owner=owner,
                           items=lists, login_session=login_session)



@app.route('/topten/new', methods=['GET', 'POST'])
@login_required
def createNewList():
    """ Returns page form for creating a new list """
    owner_id = login_session['user_id']
    owner = session.query(Owner).filter_by(id=owner_id).one()
    if request.method == 'POST':
        newList = Lists(name=request.form['name'],
                        description=request.form['description'],
                        pic_url=request.form['pic'], owner_id=owner_id,
                        published = datetime.today(), 
                        updated=datetime.today())
        session.add(newList)
        session.commit()
        flash('New List Created, ' + newList.name + ' has been added!!')
        return redirect(url_for('ownerLists', owner_id=owner_id))
    else:
        return render_template('createNewList.html', owner_id=owner_id)


@app.route('/topten/<int:owner_id>/<int:tlist_id>/edit',
           methods=['GET', 'POST'])
@login_required
@user_authorized
def editList(owner_id, tlist_id):
    """ Returns page with form for editing a List """
    list_to_edit = session.query(Lists).filter_by(id=tlist_id).one()
    if request.method == 'POST':
        if not (request.form['name'] == ''):
            list_to_edit.name = request.form['name']
        if not (request.form['description'] == ''):
            list_to_edit.description = request.form['description']
        if not (request.form['pic_url'] == ''):
            list_to_edit.pic_url = request.form['pic_url']
        list_to_edit.updated = datetime.today()
        session.add(list_to_edit)
        session.commit()
        flash(list_to_edit.name + ' has been edited')
        return redirect(url_for('ownerLists', owner_id=list_to_edit.owner_id))
    else:
        return render_template('editList.html', tlist=list_to_edit)


@app.route('/topten/<int:owner_id>/<int:tlist_id>/delete',
           methods=['GET', 'POST'])
@login_required
@user_authorized
def deleteList(owner_id, tlist_id):
    """ Returns page for confirmation to delete a List including all
        children """
    list_to_delete = session.query(Lists).filter_by(id=tlist_id).one()
    if request.method == 'POST':
        session.delete(list_to_delete)
        session.commit()
        flash(list_to_delete.name + ' has been DELETED!!')
        return redirect(url_for('ownerLists', owner_id=owner_id))
    else:
        items = session.query(Items).filter_by(lists_id=tlist_id).all()
        return render_template('deleteList.html', tlist=list_to_delete,
                                items=items)


# '  Start of Pages for working with items  '#
@app.route('/topten/<int:owner_id>/<int:tlist_id>/')
def topTenItems(owner_id, tlist_id):
    """ Returns page for showing items in a list """
    items = session.query(Items).filter_by(lists_id=tlist_id).order_by('rank').all()
    tlist = session.query(Lists).filter_by(id=tlist_id).one()
    return render_template('topTenItems.html', tlist=tlist, items=items,
                           login_session=login_session)


@app.route('/topten/<int:owner_id>/<int:tlist_id>/new',
           methods=['GET', 'POST'])
@login_required
@user_authorized
def createNewItem(owner_id, tlist_id):
    """ Returns a page with form for creating an item """
    tlist = session.query(Lists).filter_by(id=tlist_id).one()
    if request.method == 'POST':
        newItem = Items(name=request.form['name'], 
                        description=request.form['description'],
                        pic_url=request.form['pic_url'], lists_id=tlist_id,
                        rank=request.form['rank'], 
                        published=datetime.today(),
                        updated=datetime.today())
        session.add(newItem)
        session.commit()
        flash('New Item Created, ' + newItem.name + ' has been added!!')
        return redirect(url_for('topTenItems', owner_id=owner_id,
                                tlist_id=tlist_id))
    else:
        tlist = session.query(Lists).filter_by(id=tlist_id).one()
        return render_template('createNewItem.html', tlist=tlist)


@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
@login_required
@user_authorized
def editItem(owner_id, tlist_id, item_id):
    """ Returns a page with form for editing an item """
    item_to_edit = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        if not (request.form['name'] == ''):
            item_to_edit.name = request.form['name']
        if not (request.form['description'] == ''):
            item_to_edit.description = request.form['description']
        if not (request.form['pic_url'] == ''):
            print request.form['pic_url']
            item_to_edit.pic_url = request.form['pic_url']
        if not (request.form['second_pic_url'] == ''):
            item_to_edit.second_pic_url = request.form['second_pic_url']
        if not (request.form['rank'] == ''):
            item_to_edit.rank = request.form['rank']
        item_to_edit.updated = datetime.today()
        session.add(item_to_edit)
        session.commit()
        flash(item_to_edit.name + ' has been edited')
        return redirect(url_for('topTenItems',
                                owner_id=item_to_edit.lists.owner_id,
                                tlist_id=item_to_edit.lists_id))
    else:
        return render_template('editItem.html', item=item_to_edit)


# 'This page is for DELETING item #, in list#, from author#, template 12
@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
@login_required
@user_authorized
def deleteItem(owner_id, tlist_id, item_id):
    """ Returns a page with form for deleting an item """
    item_to_delete = session.query(Items).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash(item_to_delete.name + ' has been DELETED!!')
        return redirect(url_for('topTenItems', owner_id=owner_id,
                                tlist_id=tlist_id))
    else:
        return render_template('deleteItem.html', item=item_to_delete)


# 'Section Functions
def ownerListSection(owner_id):
    """ Returns a string of html for a section showing the lists
        for a particular owner """
    lists = session.query(Lists).filter_by(owner_id=owner_id).all()
    owner = session.query(Owner).filter_by(id=owner_id).one()
    return render_template('ownerListSection.html', owner=owner,
                           items=lists, owner_id=owner.id)


# 'Helper Functions
def ownerExists(owner_id):
    owners = session.query(Owner).filter_by(id=owner_id).all()
    if owners == []:
        return False
    else:
        return True


# '  JSON API endpoints  start
@app.route('/topten/owners/json/')
def topTenOwnersJSON():
    owners = session.query(Owner).all()
    return jsonify(Owner=[i.serialize for i in owners])


@app.route('/topten/lists/json/')
def ListsJSON():
    lists = session.query(Lists).all()
    return jsonify(Lists=[i.serialize for i in lists])


@app.route('/topten/items/json/')
def itemsJSON():
    items = session.query(Items).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/topten/<int:owner_id>/lists/json/')
def ownerListsJSON(owner_id):
    lists = session.query(Lists).filter_by(owner_id=owner_id).all()
    return jsonify(Lists=[i.serialize for i in lists])


@app.route('/topten/<int:lists_id>/items/json/')
def listJSON(lists_id):
    items = session.query(Items).filter_by(lists_id=lists_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/topten/<int:item_id>/Lists/items/json/')
def itemJSON(item_id):
    items = session.query(Items).filter_by(id=item_id).all()
    return jsonify(Items=[i.serialize for i in items])
# ' End JSON API endpoints


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "My Top Ten Lists"


# 'Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px; height: 300px;
                 border-radius: 150px;-webkit-border-radius:
                 150px;-moz-border-radius: 150px;"> '"""
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = Owner(name=login_session['username'], email=login_session[
                   'email'], pic_url=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Owner).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Owner).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Owner).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# ' Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('mainPage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('mainPage'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
