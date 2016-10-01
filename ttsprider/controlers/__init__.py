from index import tt_index
from error import tt_error

def Register_Blueprints(app):
    app.register_blueprint(tt_index)
    app.register_blueprint(tt_error)
