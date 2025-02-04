from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from RM_app.models import Role, Department
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required



# Create your views here.


# REGISTER FUNCTION
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', '').strip()
        email = request.POST.get('uemail', '').strip()
        upass = request.POST.get('upass', '').strip()
        context = {}

        if not uname or not email or not upass:
            context['errmsg'] = "Please fill all the fields."
            return render(request, 'register.html', context)

        if User.objects.filter(username=uname).exists():
            context['errmsg'] = "Username already exists. Please choose a different one."
            return render(request, 'register.html', context)

        if User.objects.filter(email=email).exists():
            context['errmsg'] = "Email ID already exists. Use another Email ID."
            return render(request, 'register.html', context)

        try:
            u = User(username=uname, email=email)
            u.set_password(upass)
            u.save()

            context['successmsg'] = "User registered successfully! Please log in."
            return redirect('ulogin')

        except Exception as e:
            print("Error:", e)
            context['errmsg'] = "An error occurred during registration. Please try again."
            return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')



# LOGIN FUNCTION
def ulogin(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")  
    
    if request.method == "POST":  
        uname = request.POST.get('uname', '').strip()
        upass = request.POST.get('upass', '').strip()
        context = {}

        if not uname or not upass: 
            context['errmsg'] = "Please fill all the fields"
            return render(request, 'login.html', context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:  
                login(request, u)
                return redirect("/dashboard")
            else:  
                context['errmsg'] = "Invalid Username/Password!!"
                return render(request, 'login.html', context)

    else: 
        return render(request, 'login.html')



# LOGOUT FUNCTION
def ulogout(request):
    logout(request)
    return redirect('ulogin')



# DEPARTMENT DASHBOARD FUNCTION
@login_required
def department_dashboard(request):
    context = {}
    departments = Department.objects.all()
    context['departments'] = departments
    return render(request, 'department_dashboard.html', context)



# ROLE DASHBOARD FUNCTION
def dashboard(request):
    context = {}
    roles = Role.objects.all()
    context['roles'] = roles
    return render(request, 'dashboard.html', context)



# CREATE DEPARTMENT FUNCTION
def create_department(request):
    context = {}

    if request.method == "POST":
        dname = request.POST.get('dname')
        ddesc = request.POST.get('ddesc')

        context['dname'] = dname
        context['ddesc'] = ddesc

        if Department.objects.filter(name=dname).exists():
            messages.error(request, "Department name already exists.")
        else:
            context['department'] = Department.objects.create(name=dname, description=ddesc)
            messages.success(request, "Department created successfully.")
            return redirect('department_dashboard')

    return render(request, 'create_department.html', context)



# UPDATE DEPARTMENT FUNCTION
def update_department(request, did):
    context = {}
    department = get_object_or_404(Department, id=did)
    context['department'] = department

    if request.method == "POST":
        department.name = request.POST.get('dname')
        department.description = request.POST.get('ddesc')
        department.save()
        messages.success(request, "Department updated successfully.")
        return redirect('department_dashboard')

    return render(request, 'update_department.html', context)



# DELETE DEPARTMENT FUNCTION    
def delete_department(request, did):
    department = get_object_or_404(Department, id=did)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect('department_dashboard')



# CREATE ROLE FUNCTION
@login_required
def create_role(request):
    context = {}

    if request.method == "POST":
        rname = request.POST.get('rname')
        rdesc = request.POST.get('rdesc')

        context['rname'] = rname
        context['rdesc'] = rdesc

        # Use the correct field name `role_name` instead of `name`
        if Role.objects.filter(role_name=rname).exists():
            messages.error(request, "Role name already exists.")
        else:
            context['role'] = Role.objects.create(role_name=rname, description=rdesc)
            messages.success(request, "Role created successfully.")
            return redirect('dashboard')

    return render(request, 'create_role.html', context)



# UPDATE ROLE FUNCTION
@login_required
def update_role(request, rid):
    context = {}
    role = get_object_or_404(Role, role_id=rid)  # Use role_id instead of id
    context['role'] = role

    if request.method == "POST":
        role.role_name = request.POST.get('rname')
        role.description = request.POST.get('rdesc')
        role.save()
        messages.success(request, "Role updated successfully.")
        return redirect('dashboard')

    return render(request, 'update_role.html', context)



# DELETE DEPARTMENT FUNCTION 
@login_required   
def delete_role(request, rid):
    role = get_object_or_404(Role, role_id=rid)
    role.status = False  
    role.delete()
    messages.success(request, "Role deleted successfully.")
    return redirect('dashboard')


