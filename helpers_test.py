import unittest
from helpers import * 
class MyTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
    def test_updatefunction(self):
        self.assertEqual(update_final_scores(), 0)
    def test_get_event_date(self):
        # Provide here a valid fixture ID
        self.assertEqual(type(get_event_date(182801)), type("")) 
    def test_parse_score(self):
        #should return a list containing two integers
        self.assertEqual( parse_scores("4 - 0")[0], 4)
        self.assertEqual( parse_scores("4 - 0")[1], 0)
    def test_calculcate_score(self):
        self.assertEqual(type(calculate_score(4)), type(2)) 
    def test_update_user_score(self):
        u_id = 2
        #Be careful to user an existing user id
        self.assertEqual(assign_user_score(u_id, 10), 0)
    def test_update_user_real_score(self):
        u_id = 2
        #Be careful to user an existing user id
        self.assertEqual(assign_user_score(u_id, calculate_score(4)), 0)

    def test_prettier_time(self):
        self.assertEqual( prettier_time("2019-12-19T18:50:00+01:00") ,"19 Dec 2019 @ 18:50")

    def test_get_league_logo(self):
        self.assertEqual(type(get_logo(656)), type(" "))
    def test_pass_strength_test(self):
        mypass = 'helloGuys'
        self.assertEqual(type(pass_strength_test(mypass)), type(True))
    def test_get_used_leagues(self):
        self.assertEqual(type(get_leagues_used()), type([]))