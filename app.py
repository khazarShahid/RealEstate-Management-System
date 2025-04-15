from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'  # Use SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for Flash messages

# Initialize the database
db = SQLAlchemy(app)

# -------------------------------
# Define Database Models
# -------------------------------
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Property {self.title}>"

# -------------------------------
# Routes
# -------------------------------
@app.route('/')
def index():
    properties = Property.query.all()
    return render_template('index.html', properties=properties)

@app.route('/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        price = float(request.form['price'])
        description = request.form['description']
        owner_name = request.form['owner_name']
        contact = request.form['contact']

        new_property = Property(title=title, location=location, price=price, 
                                description=description, owner_name=owner_name, contact=contact)

        try:
            db.session.add(new_property)
            db.session.commit()
            flash("Property added successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {e}", "danger")

    return render_template('add_property.html')

@app.route('/delete/<int:id>')
def delete_property(id):
    property_to_delete = Property.query.get_or_404(id)
    try:
        db.session.delete(property_to_delete)
        db.session.commit()
        flash("Property deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")

    return redirect(url_for('index'))

# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
    with app.app_context():  # FIX: Ensure app context before creating tables
        db.create_all()  # Create tables if they don’t exist
    app.run(debug=True)
