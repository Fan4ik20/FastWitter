from fastapi import APIRouter

from routers import auth

from routers.users import users
from routers.users import user_followers

from routers.posts import user_posts
from routers.posts import posts
from routers.posts import post_likes

from routers.comments import comments
from routers.comments import post_comments
from routers.comments import user_comments


router = APIRouter(prefix='/api/v1')


router.include_router(auth.router)
router.include_router(users.router)
router.include_router(user_followers.router)
router.include_router(posts.router)
router.include_router(user_posts.router)
router.include_router(post_likes.router)
router.include_router(comments.router)
router.include_router(user_comments.router)
router.include_router(post_comments.router)
