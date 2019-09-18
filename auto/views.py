from django.shortcuts import render, redirect

def index(request):
    pass
    return render(request, 'auto/index.html')

def login(request):
    if request.method == 'POST':        # 判断请求方式是否是POST
        # 接收html中name是username和password的标签
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username == '123'and password == '123':
            # 指向首页
            return render(request, 'auto/index.html')
        else:
            # 重定向到百度
            return redirect('https://www.baidu.com')
    return render(request, 'auto/login.html')
