from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):
    """testing test"""

    def test_bad_maths(self):
        """тест: неправильные матем. расчеты"""
        self.assertEqual(1+1, 3)