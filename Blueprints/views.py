import json
from flask import Blueprint,render_template,Response,session
from flask_login import current_user,login_required
from Models import Hobby
views = Blueprint('views',__name__)

app_specific_path = 'UserFunctionTemplates_APPSPECIFIC'
@views.route('/')
def index():
    return render_template('index.html')

@views.route('/auth/<what>')
def authview(what):
    if(what=='login'):
        return render_template('loginform.html')
    elif(what=='signup'):
        return render_template('signupform.html')



@views.route('/homepage')
@login_required
def homepage():
    if(current_user.is_authenticated):
        response = Response(render_template('homepage.html',props=current_user.props))
        response.headers['Cache-control'] = 'no-cache'
        return response






@views.route('/homepage/viewuserhobby')
@login_required
def viewuserhobby():
    hobbies = current_user.getHobbies()

    return render_template(f'{app_specific_path}/viewuserhobby.html',hobbies=hobbies)



@views.route('/homepage/viewuserfriends')
@login_required
def viewuserfriends():
    return render_template(f'{app_specific_path}/viewuserfriends.html', user=current_user)


@views.route('/homepage/viewuserprogress')
@login_required
def viewuserprogress():
    return render_template(f'{app_specific_path}/viewuserprogress.html', user=current_user)



@views.route('/homepage/searchnewhobbies')
@login_required
def searchnewhobbies():
    return render_template(f'{app_specific_path}/searchnewhobbies.html', user=current_user)


@views.route('/homepage/viewuserhobby/addhobbyform')
@login_required
def HobbyForm():
    hobbies = Hobby.getall()
    return render_template(f'{app_specific_path}/addhobbyform.html',hobbies=hobbies)


@views.route('/homepage/viewuserprogress/setProgressCheck')
def setProgressCheck():
    hobbies = current_user.getHobbies()
    hobbies = list(filter(lambda a:a['ISPROGRESSCHECKACTIVE']==0, hobbies))
    lenofhobbies = len(hobbies)
    response = Response(render_template(f'{app_specific_path}/SettingNewProgressCheck.html',hobbies=hobbies,len=lenofhobbies))
    return response


@views.route('/homepage/viewuserprogress/seeProgressCheck')
def seeProgressCheck():
    hobbies = current_user.getHobbies()

    with_progress_check = list(filter(lambda a:a['ISPROGRESSCHECKACTIVE']==1,hobbies))
    print(with_progress_check)
    response = Response(render_template(f'{app_specific_path}/ViewAvailableProgress.html',hobbies=with_progress_check,length=len(with_progress_check)))
    return response


@views.route('/error')
def errorpage():
    return -100



@views.route('/homepage/viewuserfriends/viewfriends')
@login_required
def viewfriends():
    all_friends = current_user.get_friends()
    response = Response(render_template(f'{app_specific_path}/listoffriends.html',friends=all_friends))

    return response

@views.route('/homepage/viewuserfriends/viewfriendsuggestions')
@login_required
def viewfriendsuggestions():
    response = Response(render_template(f'{app_specific_path}/findfriends.html'))
    return response

@views.route('/homepage/viewuserfriends/viewuseravailable')
@login_required
def viewuseravailable():
    users_available = session.get('usersavailable',[])
    return Response(render_template(f'{app_specific_path}/viewuseravailable.html',users=users_available))
