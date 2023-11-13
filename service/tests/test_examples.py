from django.test import TestCase


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print(
            "\nMethod setUpTestData is run once at the beginning of the test case for "
            "class level setup, it creates unmodified data for all remaining test "
            "methods."
        )
        pass

    def setUp(self):
        print(
            "\nMethod setUp is run once before every test method to setup clean data."
        )
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        # Will be marked as successful (i.e. test passed):
        # a dot (.) will appear
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        # Will be marked as failed:
        # an (F) will appear
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        # Will be marked as successful (test passed).
        # a dot (.) will appear
        self.assertEqual(1 + 1, 2)
