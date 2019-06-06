#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 runtarou <runtarou.com@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import logging
import os
from pathlib import Path

import yaml
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo

import kanilog
import stdlogging


def main():
    blog_settings = yaml.load(Path('./blog.yml').read_text())
    wp = Client(blog_settings['xmlrpc-url'], blog_settings['username'], blog_settings['password'])
    articles = wp.call(GetPosts())

    [article.title for article in articles]

    post = WordPressPost()
    post.title = 'My new title'
    post.content = 'This is the body of my new post.'
    wp.call(NewPost(post))

    post.post_status = 'publish'
    wp.call(EditPost(post.id, post))


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    kanilog.setup_logger(logfile='/tmp/%s.log' % (Path(__file__).name), level=logging.INFO)
    stdlogging.enable()
    main()
