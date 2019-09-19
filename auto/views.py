from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from auto.models import User
import time
from functools import wraps

def check_login(f):
    """说明：这个装饰器的作用，就是在每个视图函数被调用时，都验证下有没法有登录，
    如果有过登录，则可以执行新的视图函数，
    否则没有登录则自动跳转到登录页面
    """
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

def login(request):
    # 判断请求方式是否是POST
    if request.method == 'POST':
        # 接收html中name是username和password的标签
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # 查询用户是否在数据库中
        user = User.objects.filter(u_name=username, u_password=password)
        print(user)
        if user:
            # 登录成功
            request.session['is_login'] = '1'  # 这个session是用于后面访问每个页面（即调用每个视图函数时要用到，用此判断是否已经登录）
            # request.session['username']=username  # 这个要存储的session是用于后面，每个页面上要显示出来，登录状态的用户名用。
            # 说明：如果需要在页面上显示出来的用户信息太多（有时还有积分，姓名，年龄等信息），所以我们可以只用session保存user_id
            request.session['user_id'] = user[0].id
            table = User.objects.get(u_name=username)       # 获取当前用户
            table.u_last_time = time.strftime('%Y-%m-%d %H:%M:%S')       # 获取用户最后一次登录时间
            table.save()     # 保存数据到数据表中
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponse("用户密码错误")
    elif request.method == 'GET':       # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
        return render(request, 'login.html')

@check_login
def index(request):
    user_id = request.session.get('user_id')
    # 使用user_id去数据库中找到对应的user信息
    userobj = User.objects.filter(id=user_id)
    print(userobj)
    if userobj:
        return render(request, 'index.html', {"user": userobj[0]})
    else:
        return render(request, 'index.html', {'user', '匿名用户'})

def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/login/')
        request.session.flush()     # 清掉session
        return response