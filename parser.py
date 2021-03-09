import requests
import config

class Comment:
    def __init__(self, comment):
        self.id = comment["id"]
        self.author = comment["author"]
        self.body = comment["body"]


class Author:
    def __init__(self, author):
        self.id = author["id"]
        self.first_name = author["first_name"]
        self.last_name = author["last_name"]
        self.email = author["email"]
        self.username = author["username"]


class Post:
    def __init__(self, post):
        self.id = post["id"]
        self.author_id = post["author_id"]
        self.like_count = post["like_count"]
        self.title = post["title"]
        self.slug = post["slug"]
        self.body = post["body"]
        self.status = post["status"]
        self.created = post["created"]
        self.updated = post["updated"]

        self.author = Author(post["author"])
        self.comments = [Comment(comment) for comment in post["comments"]]

    def like(self, user_id):
        return requests.post(url=f"{config.POST_API}{self.id}/like/", data={'session_key': user_id})
# прив'язувати лайк до ід користувача
