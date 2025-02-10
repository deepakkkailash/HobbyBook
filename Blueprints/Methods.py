import json

from flask import Blueprint,request,redirect,url_for
from flask_login import current_user,login_required
from Models import Hobby
methods = Blueprint('methods',__name__)

@methods.route('/addHobbyforUser',methods=['POST'])
@login_required
def addHobby():
    data = request.form
    current_user.addHobbies(data['hobbyname'])
    return redirect(url_for('views.viewuserhobby'));


@methods.route('/setCheckonHobby',methods=['POST'])
@login_required
def setCheckonHobby():
    data = request.form
    print(data)
    res = current_user.setProgressCheckonHobby(data['hobbyname'])
    if(res!=200):
        return redirect(url_for('views.errorpage'))
    else:
        return redirect(url_for('views.homepage'))


@methods.route('/searchhobbydetails',methods=['POST'])
@login_required
def searchhobbydetails():
    form = request.json
    hobby = form['hobbyname']
    hobbydetails = Hobby.searchhobby(hobby)

    if(hobbydetails['hobbyname']!='NotFound'):
        output = {'statusCode':200,'hobbydetails':hobbydetails}
    else:
        output = {'statusCode': 500, 'hobbydetails': 'No Hobby Found'}

    return json.dumps(output)