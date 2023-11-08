from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.models import User, Destination
from app.forms import LoginForm, RegistrationForm, DestinationForm
import requests

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    destinations = Destination.query.order_by(Destination.created_at.desc()).all()
    return render_template('index.html', destinations=destinations)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)




@bp.route('/search')
def search():
    query = request.args.get('query')
    destinations = []
    if query:
        response = requests.get('API_ENDPOINT', params={'query': query}, headers={'Authorization': 'Bearer YOUR_API_KEY'})
        if response.ok:
            # Assuming the API returns a JSON response with a list of destinations
            destinations_data = response.json()
            # You would then process this data and extract the destinations
            destinations = process_destinations_data(destinations_data)
        else:
            flash('There was an error with the API request')
    else:
        flash('No query provided for search')

    return render_template('search_results.html', destinations=destinations)






@bp.route('/external-api')
def external_api():
    # Replace 'your_api_key' and 'API_ENDPOINT' with actual values
    headers = {
        'Authorization': 'Bearer your_api_key'
    }
    response = requests.get('API_ENDPOINT', headers=headers)
    
    # Handle potential errors with try/except block
    try:
        response.raise_for_status()
        # Process the response data as needed
        data = response.json()
        return jsonify(data)
    except requests.exceptions.HTTPError as e:
        # Return the error message or code
        return jsonify(error=str(e)), response.status_code

if __name__ == '__main__':
    bp.run(debug=True)





# ... include the existing destination CRUD routes, ensuring they're protected with @login_required where appropriate ...

# You will need to add the templates for login.html and register.html
# Additionally, you will need to add forms for creating and editing destinations
# And ensure that the `current_user` is checked for their operations and collections
