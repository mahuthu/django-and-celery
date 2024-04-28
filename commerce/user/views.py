from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .forms import LoginForm
from django.core.cache import cache




@csrf_exempt
def user_list(request):
    if request.method == "GET":
        users = Customer.objects.all()[:10]
        user_list = []
        for user in users:
            user_dict = {
                "customer_id": user.customer_id,
                "first_name": user.first_name,
                "phone": user.phone,
                "email": user.email,
            }

            user_list.append(user_dict)
        return JsonResponse(user_list, safe=False)
    elif request.method == "POST":
        data = request.POST
        new_user = Customer.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email")

        )

        return JsonResponse({"message": "user created successfully"}, status = 201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(username = username, email = email, password = password)
            login(request, user)
            return redirect("home")
        else:
            form = RegistrationForm
        return render(request, "register/register.html", {"form":form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                form.add_error(None, "invalid username or password")
        else:
            form = LoginForm:
        return render(request, "register/login.html", {"form":form})

def customer_view(request, customer_id):
    if customer_id == 10:
        cached_customer = cache.get("customer_10_data")
        if cached_customer:
            return render(request, 'customer.html', {"customer": cached_customer})
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        return render(request, 'customer.html', {"customer": customer})
    except Customer.DoesNotExist:
        return render(request, "error.html", {"message": "Customer not found"})



# from django.http import HttpResponse
#
# def customer_view(request, customer_id):
#     if customer_id == 10:
#         cache_key = f'customer_{customer_id}_data'
#         cached_data = cache.get(cache_key)
#         if cached_data:
#             return HttpResponse(cached_data)
#
#         # Simulated customer data retrieval from database
#         customer_data = f"Customer ID: {customer_id}, Name: John Doe, Email: johndoe@example.com"
#         cache.set(cache_key, customer_data, timeout=300)  # Cache response for 5 minutes
#         return HttpResponse(customer_data)
#     else:
#         return HttpResponse("Customer not found or caching disabled for this customer ID.")