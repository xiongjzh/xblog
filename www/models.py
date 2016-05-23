#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, uuid
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField,FloatField,TextField

with open('transwarp/schema.sql', 'w') as f:
	t=time.asctime(time.localtime(time.time()))
	f.write('-- init database \n-- generated at %s\n' % t)
	f.write("drop database if exists xblog;\ncreate database xblog;\nuse xblog;\ngrant select, insert, update, delete on xblog.* to 'root'@'localhost' identified by 'xjzh256874';\n")

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=False, ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(updatable=False, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)


with open('transwarp/schema.sql', 'a') as f:
	f.write(User().__sql__()+'\n'+Blog().__sql__()+'\n'+Comment().__sql__())

if __name__=='__main__':
    import doctest
    doctest.testmod()