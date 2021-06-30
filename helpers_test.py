import unittest, json
from helpers import push_response_to_db

class MyTest(unittest.TestCase):
    
    def test_json_to_database(self):

        json_fixtures_response_example = '''
        
        {"get":"fixtures","parameters":{"league":"4","season":"2020","next":"50"},"errors":[],"results":4,"paging":{"current":1,"total":1},"response":[{"fixture":{"id":718243,"referee":null,"timezone":"UTC","date":"2021-07-02T16:00:00+00:00","timestamp":1625241600,"periods":{"first":null,"second":null},"venue":{"id":null,"name":"Saint-Petersburg Stadium","city":"St. Petersburg"},"status":{"long":"Not Started","short":"NS","elapsed":null}},"league":{"id":4,"name":"Euro Championship","country":"World","logo":"https:\/\/media.api-sports.io\/football\/leagues\/4.png","flag":null,"season":2020,"round":"Quarter-finals"},"teams":{"home":{"id":15,"name":"Switzerland","logo":"https:\/\/media.api-sports.io\/football\/teams\/15.png","winner":null},"away":{"id":9,"name":"Spain","logo":"https:\/\/media.api-sports.io\/football\/teams\/9.png","winner":null}},"goals":{"home":null,"away":null},"score":{"halftime":{"home":null,"away":null},"fulltime":{"home":null,"away":null},"extratime":{"home":null,"away":null},"penalty":{"home":null,"away":null}}},{"fixture":{"id":718242,"referee":null,"timezone":"UTC","date":"2021-07-02T19:00:00+00:00","timestamp":1625252400,"periods":{"first":null,"second":null},"venue":{"id":700,"name":"Allianz Arena","city":"M\u00fcnchen"},"status":{"long":"Not Started","short":"NS","elapsed":null}},"league":{"id":4,"name":"Euro Championship","country":"World","logo":"https:\/\/media.api-sports.io\/football\/leagues\/4.png","flag":null,"season":2020,"round":"Quarter-finals"},"teams":{"home":{"id":1,"name":"Belgium","logo":"https:\/\/media.api-sports.io\/football\/teams\/1.png","winner":null},"away":{"id":768,"name":"Italy","logo":"https:\/\/media.api-sports.io\/football\/teams\/768.png","winner":null}},"goals":{"home":null,"away":null},"score":{"halftime":{"home":null,"away":null},"fulltime":{"home":null,"away":null},"extratime":{"home":null,"away":null},"penalty":{"home":null,"away":null}}},{"fixture":{"id":718186,"referee":null,"timezone":"UTC","date":"2021-07-03T16:00:00+00:00","timestamp":1625328000,"periods":{"first":null,"second":null},"venue":{"id":2607,"name":"Bak\u0131 Olimpiya Stadionu","city":"Baku"},"status":{"long":"Not Started","short":"NS","elapsed":null}},"league":{"id":4,"name":"Euro Championship","country":"World","logo":"https:\/\/media.api-sports.io\/football\/leagues\/4.png","flag":null,"season":2020,"round":"Quarter-finals"},"teams":{"home":{"id":770,"name":"Czech Republic","logo":"https:\/\/media.api-sports.io\/football\/teams\/770.png","winner":null},"away":{"id":21,"name":"Denmark","logo":"https:\/\/media.api-sports.io\/football\/teams\/21.png","winner":null}},"goals":{"home":null,"away":null},"score":{"halftime":{"home":null,"away":null},"fulltime":{"home":null,"away":null},"extratime":{"home":null,"away":null},"penalty":{"home":null,"away":null}}},{"fixture":{"id":718252,"referee":null,"timezone":"UTC","date":"2021-07-03T19:00:00+00:00","timestamp":1625338800,"periods":{"first":null,"second":null},"venue":{"id":910,"name":"Stadio Olimpico","city":"Roma"},"status":{"long":"Not Started","short":"NS","elapsed":null}},"league":{"id":4,"name":"Euro Championship","country":"World","logo":"https:\/\/media.api-sports.io\/football\/leagues\/4.png","flag":null,"season":2020,"round":"Quarter-finals"},"teams":{"home":{"id":772,"name":"Ukraine","logo":"https:\/\/media.api-sports.io\/football\/teams\/772.png","winner":null},"away":{"id":10,"name":"England","logo":"https:\/\/media.api-sports.io\/football\/teams\/10.png","winner":null}},"goals":{"home":null,"away":null},"score":{"halftime":{"home":null,"away":null},"fulltime":{"home":null,"away":null},"extratime":{"home":null,"away":null},"penalty":{"home":null,"away":null}}}]}
        
        
        '''


        loaded_json = json.loads(json_fixtures_response_example)


        for fixture in loaded_json["response"]: 

            print("Fixture ID : ", fixture["fixture"]['id'])
            print("Fixture time : ", fixture["fixture"]['date'])
            print(fixture["teams"]['home']['name'])
            print("VS.")
            print(fixture["teams"]['away']['name'])
            print(fixture["fixture"]['venue']['name'])
            print(fixture["fixture"]['venue']['city'])





        
    # def test_updatefunction(self):
    #     self.assertEqual(update_final_scores(), 0)
    # def test_get_event_date(self):
    #     # Provide here a valid fixture ID
    #     self.assertEqual(type(get_event_date(182801)), type("")) 
    # def test_parse_score(self):
    #     #should return a list containing two integers
    #     self.assertEqual( parse_scores("4 - 0")[0], 4)
    #     self.assertEqual( parse_scores("4 - 0")[1], 0)
    # def test_calculcate_score(self):
    #     self.assertEqual(type(calculate_score(4)), type(2)) 
    # def test_update_user_score(self):
    #     #Be careful to user an existing user id
    #     self.assertEqual(assign_user_score(6, 10), 0)
    # def test_update_user_real_score(self):
    #     #Be careful to user an existing user id
    #     self.assertEqual(assign_user_score(6, calculate_score(4)), 0)

    # def test_prettier_time(self):
    #     self.assertEqual( prettier_time("2019-12-19T18:50:00+01:00") ,"19 Dec 2019 @ 18:50")

    # def test_get_league_logo(self):
    #     self.assertEqual(type(get_logo(656)), type(" "))

if __name__ == '__main__':
    unittest.main()