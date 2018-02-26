# coding: utf-8
import sys

import tornado.web
import tornado.httpserver
import tornado.ioloop

from models.settings import Model
import config


class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, config.routes, **config.SITE_SETTINGS['settings'])


def setup():
    try:
        db = config.db.init(config.APPLICATION_SETTINGS['database'])
        config.db.Base.metadata.create_all(db.bind)  # create table structure
        user = raw_input('Blog user: ').strip()  # blog username
        pwd = raw_input('Blog password: ').strip()  # blog password
        title = raw_input('Blog title: ').strip()  # blog title
        record = db.query(Model).first()
        if not record:
            temp = Model(site_title=title, user_name=user, user_pwd=pwd, page_number=10)
            db.add(temp)
        else:
            record.site_title = title
            record.user_name = user
            record.user_pwd = pwd
            record.page_number = 10
        db.commit()
        print 'Successful installation!'
        exit(0)
    except Exception, e:
        if hasattr(e, 'orig'):
            print e.orig.args
        else:
            print e
        exit(-1)


def main():
    server = tornado.httpserver.HTTPServer(Application(), ssl_options=config.SITE_SETTINGS.get('ssl', None))
    server.listen(config.SITE_SETTINGS['port'], config.SITE_SETTINGS['host'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    setup()
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        setup()
    else:
        main()
