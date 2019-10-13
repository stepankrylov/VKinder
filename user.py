import vk
from pymongo import MongoClient
import time
import datetime
from datetime import date


def user(token, id):

        client = MongoClient()
        mongo_friends_db = client['friends']
        client.drop_database(mongo_friends_db)
        
        session = vk.Session(access_token=token)
        vk_api = vk.API(session, v='5.89')
        z = vk_api.users.get(
                             user_ids=id,
                             fields='''
                                         bdate,
                                         city,
                                         interests, 
                                         music, 
                                         movies, 
                                         books
                                    ''', 
                             )
        
        today = date.today()
        year = int(z[0]['bdate'].split('.')[2])
        month = int(z[0]['bdate'].split('.')[1])
        day = int(z[0]['bdate'].split('.')[0])
        born = datetime.date(year, month, day)
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        city = z[0]['city']['id']

        client = MongoClient()
        mongo_friends_db = client['friends']
        friends_collection = mongo_friends_db.friends

        x = vk_api.users.search(
                                age_from=age-5,
                                age_to=age,
                                city=city, 
                                is_closed=False,
                                can_access_closed=True,
                                has_photo=1,
                                sex=1,
                                fields='''
                                        bdate, 
                                        photo_max_orig, 
                                        photo_id, 
                                        common_count, 
                                        interests, 
                                        music, 
                                        movies, 
                                        books
                                       ''', 
                                count=1000
                                )
        friends = x['items']

        pause = 0.34
        list_friends = []
        for item in friends:
            if item['is_closed'] == False and item['can_access_closed'] == True:
                try:
                    y = vk_api.photos.get(
                                          owner_id=item['photo_id'].split('_')[0], 
                                          photo_ids=item['photo_id'].split('_')[1], 
                                          album_id='profile', 
                                          extended=1
                                         )
                except KeyError:
                    pass

                try:
                    dict_friend = {
                                    'id': item['id'], 
                                    'first_name': item['first_name'],
                                    'last_name': item['last_name'],
                                    'bdate': item.get('bdate', ''),
                                    'photo': item['photo_max_orig'],
                                    'count_likes_photo': y['items'][0]['likes']['count'],
                                    'common_count': item['common_count'],
                                    'interests': item.get('interests', ''),
                                    'music': item.get('music', ''),
                                    'movies': item.get('movies', ''),
                                    'books': item.get('books', '')
                                    }
                    print(dict_friend)
                    list_friends.append(dict_friend)                
                except IndexError:
                    pass

                time.sleep(pause)
        friends_collection.insert_many(list_friends)
