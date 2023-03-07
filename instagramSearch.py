# # Download Posts in a Specific Period
# import instaloader
#
# from datetime import datetime
# from itertools import dropwhile, takewhile
#
# L = instaloader.Instaloader()
#
# posts = instaloader.Profile.from_username(L.context, "instagram").get_posts()
#
# SINCE = datetime(2015, 5, 1)
# UNTIL = datetime(2015, 3, 1)
#
# for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
#     print(post.date)
#     L.download_post(post, "instagram")
#
# # # Top X Posts of User
# # from itertools import islice
# # from math import ceil
# #
# # from instaloader import Instaloader, Profile
# #
# # PROFILE = ...        # profile to download from
# # X_percentage = 10    # percentage of posts that should be downloaded
# #
# # L = Instaloader()
# #
# # profile = Profile.from_username(L.context, PROFILE)
# # posts_sorted_by_likes = sorted(profile.get_posts(),
# #                                key=lambda p: p.likes + p.comments,
# #                                reverse=True)
# #
# # for post in islice(posts_sorted_by_likes, ceil(profile.mediacount * X_percentage / 100)):
# #     L.download_post(post, PROFILE)