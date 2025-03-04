import secrets
from flask import Flask
from Blueprints.views import  views
from Blueprints.auth import auth
from Blueprints.Methods import methods
from flask_login import LoginManager
from Models import User



app = Flask(__name__)


app.secret_key = secrets.token_hex(32)
lm = LoginManager()

lm.init_app(app)

lm.login_view = 'views.index'


app.register_blueprint(views)
app.register_blueprint(auth)
app.register_blueprint(methods)


@lm.user_loader
def loaduser(userid):
    return User.loaduserusingusername(userid)

if(__name__=='__main__'):
    app.run(debug=True)

