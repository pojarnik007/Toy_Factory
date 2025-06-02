from django.test import TestCase
from reviews.models import Review
from users.models import User

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create()

    def test_model_creation(self):
        review = Review.objects.create(
            title='Test Review',
            text='This is a test review.',
            rating=5,
            user=self.user
        )
        self.assertEqual(review.title, 'Test Review')
        self.assertEqual(review.text, 'This is a test review.')
        self.assertEqual(review.rating, 5)

# Add similar test cases for views and forms here
