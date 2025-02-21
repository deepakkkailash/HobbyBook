import json

from flask import Blueprint,request,redirect,url_for
from flask_login import current_user,login_required
from Models import Hobby
methods = Blueprint('methods',__name__)

@methods.route('/addHobbyforUser',methods=['POST'])
@login_required
def addHobby():
    data =list(request.form.values())
    print(data)
    current_user.addHobbies(data[0],data[1:]);
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


@methods.route('/getMilestones',methods=['POST'])
@login_required
def getmilestones():
    data = request.json
    hobbyname = data['hobbyname']
    print(hobbyname)
    milestones = current_user.getMilestones(hobbyname)['MILESTONES']
    if(milestones==None):
        return json.dumps({'milestones':'NotFound'})
    else:
        milestones = milestones.split(',')
    return json.dumps({'milestones':milestones})


@methods.route('/updateprogressformilestones',methods=['POST'])
@login_required
def updatemilestoneprogress():
    form = request.json
    milestone_progress = form['milestones'][0]
    print(milestone_progress)
    target_hobby = form['targethobby']
    if(current_user.updateMilestones(milestone_progress,target_hobby)):
        return json.dumps({'statuscode':200})
    else:
        return json.dumps({'statuscode':500})
