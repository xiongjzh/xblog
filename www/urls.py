#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.web import get, view, post, ctx,interceptor
from models import User, Blog, Comment
from apis import api,APIValueError,APIError,Page
import logging,re,hashlib,time

@view('test_users.html')
@get('/test')
def test_users():
    users = User.find_all()
    return dict(users=users)

@view('blogs.html')
@get('/')
def index():
    blogs = Blog.find_all()
    # 查找登陆用户:
    # user = User.find_first('where email=?', 'admin@example.com')
    return dict(blogs=blogs, user=ctx.request.user)

@api
@get('/api/users')
def api_get_users():
    users = User.find_by('order by created_at desc')
    # 把用户的口令隐藏掉:
    for u in users:
        u.password = '******'
    return dict(users=users)

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
#注册
@view('register.html')
@get('/register')
def get_register():
	return dict()

@api
@post('/api/user/register')
def register_user():
    i = ctx.request.input(name='', email='', password='')
    name = i.name.strip()
    email = i.email.strip().lower()
    password = i.password
    if not name:
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_MD5.match(password):
        raise APIValueError('password')
    user = User.find_first('where email=?', email)
    if user:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(name=name, email=email, password=password, image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
    user.insert()
    return user

@view('blogs.html')
@get('/signout')
def get_signout():
    ctx.response.delete_cookie('auth')
    blogs = Blog.find_all()
    return dict(blogs=blogs, user=None)

@view('signIn.html')
@get('/signin')
def get_signin():
    return dict(user=None)

@api
@post('/api/user/signin')
def signin_user():
    i = ctx.request.input()
    email = i.email.strip().lower()
    password = i.password
    user = User.find_first('where email=?', email)
    if user is None:
        raise APIError('auth:failed', 'email', 'Invalid email.')
    elif user.password != password:
        raise APIError('auth:failed', 'password', 'Invalid password.')
    max_age = 604800
    cookie = make_signed_cookie(user.id, user.password, max_age)
    ctx.response.set_cookie('auth', cookie, max_age=max_age)
    user.password = '******'
    return user
def make_signed_cookie(id, password, max_age):
    expires = str(int(time.time() + max_age))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, 'chasecho')).hexdigest()]
    return '-'.join(L)
@interceptor('/')
def auth_interceptor(next):
    user = None
    cookie = ctx.request.cookies.get('auth')
    if cookie:
        user = parse_signed_cookie(cookie)
    ctx.request.user = user
    return next()
def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        id, expires, md5 = L
        if int(expires) < time.time():
            return None
        user = User.get(id)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, 'chasecho')).hexdigest():
            return None
        return user
    except:
        return None

#blog创建
@view('blog_edit.html')
@get('/newblog')
def get_newblog():
    return dict(user=ctx.request.user,action='/api/blogs',redirect='/')

@api
@post('/api/blogs')
def api_create_blog():
    i = ctx.request.input(name='', summary='', content='')
    name = i.name.strip()
    summary = i.summary.strip()
    content = i.content.strip()
    if not name:
        raise APIValueError('name', 'name cannot be empty.')
    if not summary:
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content:
        raise APIValueError('content', 'content cannot be empty.')
    user = ctx.request.user
    blog = Blog(user_id=user.id, user_name=user.name, name=name, summary=summary, content=content)
    blog.insert()
    return blog

#blog分页，列表
def _get_page_index():
    page_index = 1
    try:
        page_index = int(ctx.request.get('page', '1'))
    except ValueError:
        pass
    return page_index

def _get_blogs_by_page():
    total = Blog.count_all()
    page = Page(total, _get_page_index())
    blogs = Blog.find_by('order by created_at desc limit ?,?', page.offset, page.limit)
    return blogs, page

@api
@get('/api/blogs')
def api_get_blogs():
    blogs, page = _get_blogs_by_page()
    logging.info(blogs)
    logging.info(page)
    logging.info(dict(blogs=blogs, page=page))
    return dict(blogs=blogs, page=page)


@view('blog_list.html')
@get('/manage/blogs')
def manage_blogs():
    return dict(page_index=_get_page_index(), user=ctx.request.user)