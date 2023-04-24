import instaloader
import config

import os
from shutil import move, rmtree

g_ig_username = ''


def get_ig_downloaded_source():
    global g_ig_username
    current_directory = os.getcwd()
    path = os.path.join(current_directory, g_ig_username)
    dir_list = os.listdir(path)
    for file_name in dir_list:
        if (".txt" in file_name) or (".jpg" in file_name):
            move(os.path.join(path, file_name), os.path.join(current_directory, file_name))
    rmtree(path)
    new_dir_list = os.listdir(current_directory)
    print(new_dir_list)


def download_last_x_publications(ig_username, pictures_number):
    global g_ig_username
    g_ig_username = ig_username
    L = instaloader.Instaloader()
    L.login(config.instagram_username, config.instagram_password)
    profile = instaloader.Profile.from_username(L.context, ig_username)
    posts_sorted_by_date = sorted(profile.get_posts(), key=lambda post: post.date, reverse=True)
    selected_range = posts_sorted_by_date[0:pictures_number]
    for post in selected_range:
        L.download_post(post, ig_username)
    get_ig_downloaded_source()


def download_top_x_publications(ig_username, pictures_number):
    global g_ig_username
    g_ig_username = ig_username
    L = instaloader.Instaloader()
    L.login(config.instagram_username, config.instagram_password)
    profile = instaloader.Profile.from_username(L.context, ig_username)
    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)
    selected_range = posts_sorted_by_likes[0:pictures_number]
    for post in selected_range:
        L.download_post(post, ig_username)
    get_ig_downloaded_source()


def download_specific_publication(ig_username, picture_number):
    global g_ig_username
    g_ig_username = ig_username
    L = instaloader.Instaloader()
    L.login(config.instagram_username, config.instagram_password)
    profile = instaloader.Profile.from_username(L.context, ig_username)
    posts_sorted_by_date = sorted(profile.get_posts(), key=lambda post: post.date, reverse=True)
    selected_publication = posts_sorted_by_date[picture_number - 1]
    L.download_post(selected_publication, ig_username)
    get_ig_downloaded_source()


# download_top_x_publications("stas_di55ik", 2)