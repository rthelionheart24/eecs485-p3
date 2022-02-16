"""Insta485 REST API."""

from insta485.api.posts import get_post_by_id
from insta485.api.posts import get_posts_by_args
from insta485.api.likes import like, unlike
from insta485.api.comments import comment, uncomment
from insta485.api.index import service_list
