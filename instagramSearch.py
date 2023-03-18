import instaloader
import config


def download_last_x_publications(ig_username, pictures_number):
    L = instaloader.Instaloader()
    L.login(config.instagram_username, config.instagram_password)
    profile = instaloader.Profile.from_username(L.context, ig_username)
    posts_sorted_by_date = sorted(profile.get_posts(), key=lambda post: post.date, reverse=True)
    selected_range = posts_sorted_by_date[0:pictures_number]
    for post in selected_range:
        L.download_post(post, ig_username)


def download_top_x_publications(ig_username, pictures_number):
    L = instaloader.Instaloader()
    L.login(config.instagram_username, config.instagram_password)
    profile = instaloader.Profile.from_username(L.context, ig_username)
    posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)
    selected_range = posts_sorted_by_likes[0:pictures_number]  # to download from only 2 posts
    for post in selected_range:
        L.download_post(post, ig_username)


def download_specific_publication(ig_username, picture_number):
    L = instaloader.Instaloader()
    L.login(config.instagram_username, config.instagram_password)
    profile = instaloader.Profile.from_username(L.context, ig_username)
    posts_sorted_by_date = sorted(profile.get_posts(), key=lambda post: post.date, reverse=True)
    selected_publication = posts_sorted_by_date[picture_number - 1]
    L.download_post(selected_publication, ig_username)
