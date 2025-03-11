import json

from flask import Blueprint,request,redirect,url_for,session,render_template,render_template_string
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


@methods.route('/searchhobbydetails',methods=['GET','POST'])
@login_required
def searchhobbydetails():
    if(request.method=='GET'):
        hobby = request.args.get('hobby')
    else:
        form = request.json
        hobby = form['hobbyname']
    hobbydetails = Hobby.searchhobby(hobby)

    template_string = """
    {% extends 'base.html' %}
    {% block content %}
    <div class='bg-black w-[100vw] h-[100vh] justify-center items-center flex flex-col '>
    <h1 class='font-mono text-5xl text-white font-bold tracking-widest'>{{hobbyname}}</h1>
    <h2 class='font-mono text-lg text-red-500 font-bold'>{{hobbytype}}</h2>
    <h4 class='font-mono text-sm text-white font-bold'>Number of users: {{numberOfUsers}}</h4>
    </div>
    {% endblock %}
                        """
    if(hobbydetails['hobbyname']!='NotFound'):
        if(request.method=='POST'):
            output = {'statusCode':200,'hobbydetails':hobbydetails}
        elif(request.method=='GET'):
            return render_template_string(template_string,hobbyname=hobbydetails.get('hobbyname'),hobbytype=hobbydetails.get('hobbytype'),numberOfUsers=hobbydetails.get('numberOfUsers'))
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
    name = request.form.get('name')
    user = User.searchuserbyusername(name)
    if(user['username']==current_user.props['username']):
        return render_template(f'{app_specific_path}/viewuseravailable.html',user='self',trigger='username')

    return render_template(f'{app_specific_path}/viewuseravailable.html',user=user,trigger='username')


@methods.route('/viewfriendsbyhobby',methods=['POST'])
@login_required
def searchfriendsbyhobby():
    list_of_users = list(filter(lambda a:a!=None, User.searchbyhobby(request.form.get('hobby','*'))))

    for i in list_of_users:
        if(i['username']==current_user.props['username']):
            list_of_users.pop(list_of_users.index(i))

    return render_template(f'{app_specific_path}/viewuseravailable.html',users=list_of_users,trigger='hobby',lenusers=len(list_of_users))

@methods.route('/viewfriendsrandomly',methods=['GET'])
@login_required
def searchrandompeople():
    list_of_random_users = User.searchrandomusers()

    return render_template(f'{app_specific_path}/viewuseravailable.html',users=list_of_random_users,trigger='random',lenusers=len(list_of_random_users))



@methods.route('/recommendarandomhobby')
@login_required
def recommendahobby():
    hobby = Hobby.getrandom()
    return json.dumps({'hobby':hobby})

@methods.route('/addfriend',methods=['POST'])
@login_required
def addFriend():
    body = request.json
    print(body)
    if(current_user.addFriend(body['userid'])):
        return json.dumps({'status':200})
    else:
        return json.dumps({'status': 500})
