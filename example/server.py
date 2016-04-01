"""
Simple async example using Tornado:

Tornado accepts a GET request @ '/?url=' and returns the URL requested
"""
import tornado.ioloop
import tornado.web
import tornado.httpclient

import validators


def get_errors():
    return {
        'missing': 'Please pass url as a parameter',
        'invalid': 'Please pass a valid URL',
        'unresolved': 'Unable to resolve URL',
    }


class MainHandler(tornado.web.RequestHandler):

    error_msgs = get_errors()

    @tornado.web.asynchronous
    def get(self):

        def callback(response):
            self.finish(response.body)

        url = self.get_argument("url", None)
        if not url:
            raise tornado.web.HTTPError(400, self.error_msgs['missing'])
        elif not validators.url(url):
            raise tornado.web.HTTPError(400, self.error_msgs['invalid'])
        else:
            async_client = tornado.httpclient.AsyncHTTPClient()
            req = tornado.httpclient.HTTPRequest(url)

            async_client.fetch(req, callback)

    def write_error(self, status_code, **kwargs):
        err_cls, err, traceback = kwargs['exc_info']
        if err.log_message and err.log_message in self.error_msgs.values():
            self.write(
                "<html><body><h1>{}</h1></body></html>".format(
                    err.log_message))
        else:
            return super(
                MainHandler, self).write_error(status_code, **kwargs)

    # New style Python with aync and await
    # async def get(self):
    #     """Get the requested URL

    #     Return either url or appropriate error
    #     """
    #     url = self.get_argument("url", None)
    #     if not url:
    #         raise tornado.web.HTTPError(400, self.error_msgs['missing'])
    #     elif not validators.url(url):
    #         raise tornado.web.HTTPError(400, self.error_msgs['invalid'])
    #     else:
    #         async_client = tornado.httpclient.AsyncHTTPClient()
    #         try:
    #             response = await async_client.fetch(url)
    #         except tornado.web.HTTPError as error:
    #             print(error)
    #             raise tornado.web.HTTPError(500, self.error_msgs['unresolved'])
    #         except Exception as error:
    #             print(error)
    #             raise tornado.web.HTTPError(500, self.error_msgs['unresolved'])
    #         self.finish(response.body)


def initialise():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = initialise()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
