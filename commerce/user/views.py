from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer
from django.shortcuts import HttpResponse


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




