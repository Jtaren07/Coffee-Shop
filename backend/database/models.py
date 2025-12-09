import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "coffee_shop"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgresql://{}:{}@{}/{}".format("postgres", "eazye5000", "localhost:5432", database_filename)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLALchemy service
"""

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_filename
    app.config["SQLACHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

"""
Drink
a persistent drink entity, extends the base SQLALchemy Model
"""

class Drink(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)

    """
    short()
        short form representation of the Drink model
    """
    def short(self):
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
                '': self.id,
                'title': self.title,
                'recipe': short_recipe
                }

    """
    long()
        long form representation of the Drink model
    """
    def long(self):
        return {
                'id': self.id,
                'title': self.title,
                'recipe': json.loads(self.recipe)
                }
    """
    insert()
        inserts a new model into a database
        the model must have a unique name the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
            EXAMPLE
                drink = Drink(title=req_title, recipe=req_recipe)
                drink.delete()
    """
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    """
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())

