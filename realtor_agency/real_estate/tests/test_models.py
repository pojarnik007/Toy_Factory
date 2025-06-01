from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from ..models import RealEstateObject, ObjectCategory, Sale


class RealEstateObjectModelTest(TestCase):
    def setUp(self):
        self.category = ObjectCategory.objects.create(name="House")
        self.image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

    def test_slug_creation(self):
        obj = RealEstateObject.objects.create(
            title="Test House",
            description="Test description",
            location="Test location",
            price=100000.00,
            image=self.image,
        )
        obj.category.add(self.category)
        self.assertEqual(obj.slug, "test-house")

        # Проверка уникальности slug
        obj2 = RealEstateObject.objects.create(
            title="Test House",
            description="Test description 2",
            location="Test location 2",
            price=200000.00,
            image=self.image,
        )
        obj2.category.add(self.category)
        self.assertTrue(obj2.slug.startswith("test-house-"))

    def test_model_fields(self):
        obj = RealEstateObject.objects.create(
            title="Another House",
            description="Another description",
            location="Another location",
            price=150000.00,
            image=self.image,
        )
        obj.category.add(self.category)
        
        self.assertEqual(obj.title, "Another House")
        self.assertEqual(obj.description, "Another description")
        self.assertEqual(obj.location, "Another location")
        self.assertEqual(obj.price, 150000.00)
        self.assertTrue(obj.on_sale)
        self.assertEqual(obj.category.count(), 1)
        filename = obj.image.name.split("/")[-1]
        self.assertTrue(filename.startswith("test_image"))
        self.assertTrue(filename.endswith(".jpg"))

        self.assertRegex(filename, r'^test_image_.+\.jpg$')

    def test_str_representation(self):
        obj = RealEstateObject.objects.create(
            title="Test House",
            description="Test",
            location="Test",
            price=100000.00,
            image=self.image,
        )
        self.assertEqual(str(obj), "Test House")


class ObjectCategoryModelTest(TestCase):
    def test_slug_creation_and_primary_key(self):
        category = ObjectCategory.objects.create(name="Test Category")
        self.assertEqual(category.slug, "test-category")
        self.assertEqual(category.pk, "test-category")

    def test_unique_slug_generation(self):
        category1 = ObjectCategory.objects.create(name="Unique Category")
        category2 = ObjectCategory.objects.create(name="Unique Category")
        self.assertNotEqual(category1.slug, category2.slug)
        self.assertTrue(category2.slug.startswith("unique-category-"))

    def test_str_representation(self):
        category = ObjectCategory.objects.create(name="Test Category")
        self.assertEqual(str(category), "Test Category")


class SaleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = ObjectCategory.objects.create(name="House")
        self.real_estate = RealEstateObject.objects.create(
            title="Test House",
            description="Test",
            location="Test",
            price=100000.00,
            image=SimpleUploadedFile("test.jpg", b"content"),
        )
        self.real_estate.category.add(self.category)

    def test_sale_creation(self):
        sale = Sale.objects.create(
            real_estate_object=self.real_estate,
            client=self.user,
        )
        self.assertEqual(sale.real_estate_object, self.real_estate)
        self.assertEqual(sale.client, self.user)

    def test_auto_date_fields(self):
        sale = Sale.objects.create(
            real_estate_object=self.real_estate,
            client=self.user,
        )
        today = timezone.now().date()
        self.assertEqual(sale.sale_date, today)
        self.assertEqual(sale.contract_date, today)

    def test_str_representation(self):
        sale = Sale.objects.create(
            real_estate_object=self.real_estate,
            client=self.user,
        )
        expected_str = (
            f"{self.real_estate} продан клиенту {self.user} {sale.sale_date}"
        )
        self.assertEqual(str(sale), expected_str)

    def test_cascade_delete_real_estate(self):
        sale = Sale.objects.create(
            real_estate_object=self.real_estate,
            client=self.user,
        )
        self.real_estate.delete()
        with self.assertRaises(Sale.DoesNotExist):
            Sale.objects.get(id=sale.id)

    def test_cascade_delete_user(self):
        sale = Sale.objects.create(
            real_estate_object=self.real_estate,
            client=self.user,
        )
        self.user.delete()
        with self.assertRaises(Sale.DoesNotExist):
            Sale.objects.get(id=sale.id)