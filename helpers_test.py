import unittest
from helpers import update_final_scores, get_event_date
class MyTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
    def test_updatefunction(self):
        self.assertEqual(update_final_scores(), 0)
    def test_get_event_date(self):
        # valid ID : 182801
        self.assertEqual(get_event_date()) 
        