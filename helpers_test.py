import unittest
from helpers import * 
class MyTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
    def test_updatefunction(self):
        self.assertEqual(update_final_scores(), 0)
    def test_get_event_date(self):
        # valid ID : 182801
        self.assertEqual(type(get_event_date(182801)), type("")) 
    def test_parse_score(self):
        #should return a list containing two integers
        self.assertEqual( parse_scores("4 - 0")[0], 4)
        self.assertEqual( parse_scores("4 - 0")[1], 0)
    def test_calculcate_score(self):
        self.assertEqual(type(calculate_score(4)), type(2)) 

        