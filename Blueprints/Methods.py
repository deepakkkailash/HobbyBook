import json

from flask import Blueprint,request,redirect,url_for,session,render_template
from flask_login import current_user,login_required
from Models import Hobby,User
methods = Blueprint('methods',__name__)


app_specific_path = 'UserFunctionTemplates_APPSPECIFIC'
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


@methods.route('/viewfriendsbyname',methods=['POST'])
@login_required
def searchfriendbyname():
    name = request.json.get('name')
    user = User.searchuserbyusername(name)
    if(user['username']==current_user.props['username']):
        return json.dumps({'user':'self'})

    return json.dumps({'user':'not_self','content':render_template(f'{app_specific_path}/viewuseravailable.html',users=[user])})


@methods.route('/viewfriendsbyhobby',methods=['POST'])
@login_required
def searchfriendsbyhobby():
    list_of_users = list(filter(lambda a:a!=None, User.searchbyhobby(request.json.get('hobby','*'))))
    print(request.json)
    for i in list_of_users:
        if(i['username']==current_user.props['username']):
            list_of_users.pop(list_of_users.index(i))
    if(len(list_of_users)==0):
        return json.dumps({'FriendSuggestions':None})

    return json.dumps({'FriendSuggestions':'not_self','content':render_template(f'{app_specific_path}/viewuseravailable.html',users=list_of_users)})

@methods.route('/viewfriendsrandomly',methods=['GET'])
@login_required
def searchrandompeople():
    list_of_random_users = User.searchrandomusers()

    return json.dumps({'FriendSuggestions':'not_self','content':render_template(f'{app_specific_path}/viewuseravailable.html',users=list_of_random_users)})



@methods.route('/recommendarandomhobby')
@login_required
def recommendahobby():
    hobby = Hobby.getrandom()
    return json.dumps({'hobby':hobby})