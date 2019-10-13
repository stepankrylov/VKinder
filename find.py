import vk
import json
from pymongo import MongoClient
import time
import re
import datetime
from datetime import date
from collections import Counter
from operator import itemgetter

def find(token, id, list_interests, list_musics, list_movies, list_books):
        session = vk.Session(access_token=token)
        vk_api = vk.API(session, v='5.89')
        z = vk_api.users.get(
                             user_ids=id,
                             fields='''
                                         interests, 
                                         music, 
                                         movies, 
                                         books
                                    ''', 
                             )
        
        client = MongoClient()
        mongo_friends_db = client['friends']
        friends_collection = mongo_friends_db.friends

        if z[0]['interests'] == '' and z[0]['music'] == '' and z[0]['movies'] == '' and z[0]['books'] == '':
            list_count = []
            random_friends = friends_collection.aggregate([{'$sample': {'size': 10}}])
            for item in list(random_friends):
                list_count.append((item['id'], 'None'))
        else:       
            list_interests = list_interests + z[0]['interests'].split()
            list_friends_interests = []
            for interest in list_interests:
                regex = re.compile('\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*'+ interest +'\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*')
                for item in friends_collection.find({'interests': regex}):
                    list_friends_interests.append(item['id'])
            c_1 = dict(Counter(list_friends_interests))
            values_inter = []
            weight_inter = 100
            for item in c_1.values():
                values_inter.append((item/len(list_interests))*weight_inter)
            c_inter = Counter(dict(zip(c_1.keys(), values_inter)))

            list_musics = list_musics + z[0]['music'].split()
            list_friends_musics = []
            for music in list_musics:
                regex = re.compile('\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*'+ music +'\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*')
                for item in friends_collection.find({'music': regex}):
                    list_friends_musics.append(item['id'])
            c_2 = dict(Counter(list_friends_musics))
            values_music = []
            weight_music = 50
            for item in c_2.values():
                values_music.append((item/len(list_musics))*weight_music)
            c_music = Counter(dict(zip(c_2.keys(), values_music)))

            list_movies = list_movies + z[0]['movies'].split()
            list_friends_movies = []
            for movie in list_movies:
                regex = re.compile('\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*'+ movie +'\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*')
                for item in friends_collection.find({'movies': regex}):
                    list_friends_movies.append(item['id'])
            c_3 = dict(Counter(list_friends_movies))
            values_movie = []
            weight_movie = 25
            for item in c_3.values():
                values_movie.append((item/len(list_movies))*weight_movie)
            c_movie = Counter(dict(zip(c_3.keys(), values_movie)))

            list_books = list_books + z[0]['books'].split()
            list_friends_books = []
            for book in list_books:
                regex = re.compile('\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*'+ book +'\w*[ -]*\w*[ ]*\w*[ ]*\w*[ ]*\d*')
                for item in friends_collection.find({'books': regex}):
                    list_friends_books.append(item['id'])
            c_4 = dict(Counter(list_friends_books))
            values_book = []
            weight_book = 20
            for item in c_4.values():
                values_book.append((item/len(list_books))*weight_book)
            c_book = Counter(dict(zip(c_4.keys(), values_book)))

            count = dict(c_inter + c_music + c_movie + c_book)
            list_count = list(count.items())
            list_count.sort(key=lambda i: i[1], reverse=True)

        pause = 0.34
        top_10 = []
        for item in list_count[:10]:
            name = vk_api.users.get(user_ids=item[0])
            photo = vk_api.photos.get(
                                      owner_id=item[0], 
                                      album_id='profile', 
                                      extended=1
                                     )
            top_photo = []
            
            for i in photo['items']:
                top_photo.append(i['sizes'][-1]['url'])
                time.sleep(pause)
            friend = {
                      'Имя': name[0]['first_name'], 
                      'Фамилия': name[0]['last_name'], 
                      'Лучшие фото': sorted(top_photo, key=itemgetter(0), reverse=True)[:3]
                     }
            print(friend)
            top_10.append(friend)
        print(len(top_10))

        with open('top_10.json', 'w', encoding='UTF-8') as file:
            json.dump(top_10, file, ensure_ascii=False)

        return len(top_10)