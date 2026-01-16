from django.shortcuts import render
from django.http import JsonResponse
from .models import Contact

def contacts(request):
    # Если это обычный запрос, отдаем HTML каркас
    return render(request, 'contacts/contacts.html')

def get_contacts_json(request):
    # Этот метод будет вызываться через JS fetch
    contacts = Contact.objects.all()
    data = []
    for c in contacts:
        # Формируем список словарей
        data.append({
            'name': c.name,
            'description': c.description,
            'email': c.user.email,
            # В модели нет телефона, возьмем заглушку или добавьте поле в модель
            'phone': getattr(c, 'phone', '80290000000'),
            'image_url': c.image.url if c.image else ''
        })
    return JsonResponse({'data': data})