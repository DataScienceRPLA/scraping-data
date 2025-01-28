import json
import csv
import tweepy
import re

"""
MASUKAN (INPUTS):
    consumer_key, consumer_secret, access_token, access_token_secret: kode 
    yang memberi tahu Twitter bahwa kita memiliki izin untuk mengakses data ini.
    hashtag_phrase: kombinasi hashtag yang ingin dicari.

KELUARAN (OUTPUTS):
    Tidak ada, hanya menyimpan informasi tweet ke dalam file spreadsheet.
"""

def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):
    # Membuat autentikasi untuk mengakses Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Menginisialisasi API Tweepy
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Menentukan nama file spreadsheet yang akan digunakan
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

    # Membuka file spreadsheet untuk menyimpan data
    with open(f'{fname}.csv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file)

        # Menulis baris header ke dalam spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

        # Mengambil tweet yang sesuai dengan hashtag dan menyimpannya ke dalam spreadsheet
        for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase + ' -filter:retweets',
                                   lang="en", tweet_mode='extended').items(100):
            w.writerow([
                tweet.created_at,  # Waktu tweet dibuat
                tweet.full_text.replace('\n', ' '),  # Isi teks tweet
                tweet.user.screen_name,  # Username pengirim tweet
                [e['text'] for e in tweet.entities['hashtags']],  # Daftar hashtag dalam tweet
                tweet.user.followers_count  # Jumlah pengikut pengguna
            ])

    print(f"Data telah disimpan dalam file {fname}.csv")


if __name__ == '__main__':
    # Mengumpulkan input dari pengguna untuk kredensial API Twitter dan hashtag yang dicari
    consumer_key = input('Consumer Key: ')
    consumer_secret = input('Consumer Secret: ')
    access_token = input('Access Token: ')
    access_token_secret = input('Access Token Secret: ')

    hashtag_phrase = input('Hashtag Phrase: ')

    # Memanggil fungsi untuk mencari tweet berdasarkan hashtag dan menyimpan data
    search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase)
