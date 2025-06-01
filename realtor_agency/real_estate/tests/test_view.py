from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage

from users.models import User, Position
from real_estate.models import RealEstateObject, ObjectCategory, Sale
from real_estate.forms import RealEstateObjectForm
from real_estate.views import catalog

def generate_test_image():
    image_io = BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(image_io, format="JPEG")
    image_io.seek(0)
    return SimpleUploadedFile("test.jpg", image_io.read(), content_type="image/jpeg")

class CatalogViewTest(TestCase):
    def setUp(self):
        self.category = ObjectCategory.objects.create(name="House")
        self.obj1 = RealEstateObject.objects.create(
            title="House 1",
            price=100000,
            on_sale=True,
            image=SimpleUploadedFile("test.jpg", b"content")
        )
        self.obj1.category.add(self.category)
        
    def test_basic_catalog(self):
        response = self.client.get(reverse('real_estate:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "House 1")
        
    def test_search_filter(self):
        response = self.client.get(reverse('real_estate:catalog') + '?q=House')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['real_estate'],
            [self.obj1], transform=lambda x: x
        )
        
    def test_category_filter(self):
        response = self.client.get(
            reverse('real_estate:catalog') + f'?categories={self.category.slug}'
        )
        self.assertEqual(response.context['real_estate'].count(), 1)

class CreateViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass',
            position=Position.ADMIN,
            email='test2@test.test',
            phone='+375 (44) 424-44-43'
        )
        self.category = ObjectCategory.objects.create(name="Apartment")
        
    def test_create_view_access(self):
        # Неавторизованный пользователь
        response = self.client.get(reverse('real_estate:create'))
        self.assertRedirects(response, '/users/login/?next=/real_estate/create/')

        # Авторизованный пользователь с правами
        self.client.force_login(self.admin)
        response = self.client.get(reverse('real_estate:create'))
        self.assertEqual(response.status_code, 200)
        
    def test_successful_creation(self):
        self.client.force_login(self.admin)
        test_image = SimpleUploadedFile(
            "test_image.jpg", 
            b"file_content", 
            content_type="image/jpeg"
        )
        
        form_data = {
            'title': 'New House',
            'description': 'Test Description',
            'location': 'Test Location',
            'price': 1500,
            'category': [self.category.pk],
            'image': generate_test_image()
        }
        response = self.client.post(
            reverse('real_estate:create'),
            data=form_data,
            follow=True
        )
        print(response.context['form'].errors)

        self.assertRedirects(response, reverse('real_estate:edit', kwargs={'slug': 'new-house'}))
        self.assertEqual(RealEstateObject.objects.count(), 1)

class BuyViewTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username='client',
            password='testpass',
            position=Position.CLIENT,
            email='test3@test.test',
            phone='+375 (44) 422-44-43'
        )
        self.obj = RealEstateObject.objects.create(
            title="For Sale",
            price=100000,
            on_sale=True,
            image=SimpleUploadedFile("test.jpg", b"content")
        )
        
    def test_successful_purchase(self):
        self.client.force_login(self.client_user)
        response = self.client.post(
            reverse('real_estate:buy', kwargs={'slug': self.obj.slug}),
            {'confirm': 'on'},
            follow=True
        )
        self.obj.refresh_from_db()
        self.assertFalse(self.obj.on_sale)
        self.assertEqual(Sale.objects.count(), 1)
        self.assertRedirects(response, reverse('real_estate:detail', kwargs={'slug': self.obj.slug}))
        
    def test_already_sold(self):
        self.obj.on_sale = False
        self.obj.save()
        self.client.force_login(self.client_user)
        response = self.client.post(
            reverse('real_estate:buy', kwargs={'slug': self.obj.slug}),
            {'confirm': 'on'},
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Объект уже продан')

class DetailViewTest(TestCase):
    def test_detail_view(self):
        obj = RealEstateObject.objects.create(
            title="Test Object",
            price=100000,
            image=SimpleUploadedFile("test.jpg", b"content")
        )
        response = self.client.get(reverse('real_estate:detail', kwargs={'slug': obj.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], obj)

class SalesViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass',
            position=Position.ADMIN,
            email='admin@test.test',
            phone='+375 (44) 424-44-44'
        )
        self.sale = Sale.objects.create(
            real_estate_object=RealEstateObject.objects.create(
                title="Sold",
                price=100000,
                image=SimpleUploadedFile("test.jpg", b"content")
            ),
            client=User.objects.create_user(username='buyer')
        )
        
    def test_sales_list_access(self):
        # Проверка доступа для сотрудника
        employee = User.objects.create_user(
            username='employee',
            password='testpass',
            position=Position.EMPLOYEE,
            email='test4@test.test',
            phone='+375 (44) 524-44-43'
        )
        self.client.force_login(employee)
        response = self.client.get(reverse('real_estate:sales'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sold")

class DeleteViewTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin',
            password='testpass',
            position=Position.ADMIN
        )
        self.cat = ObjectCategory.objects.create(name='test')
        self.obj = RealEstateObject.objects.create(
            title="To Delete",
            image=SimpleUploadedFile("test.jpg", b"content"),
            price=100,
            location='test',
        )
        self.obj.category.add(self.cat)
        
    def test_delete_object(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('real_estate:delete', kwargs={'slug': self.obj.slug}),
            follow=True
        )
        self.assertRedirects(response, reverse('real_estate:catalog'))
        self.assertEqual(RealEstateObject.objects.count(), 0)

