import os
import json
import tornado.ioloop
import tornado.web
from decouple import config
from notebook import transutils as _
from notebook.services.contents.filemanager import FileContentsManager as FCM


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        domain = config("DOMAIN_NAME")
        self.write({"domain": domain})


class BaseRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Content-type", "application/json")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods",
        )

    def OPTIONS(self):
        pass


class JupyterNotebookHandler(BaseRequestHandler):
    def post(self):

        payload = json.loads(self.request.body)
        project = payload["project"]
        file = payload["notebook_name"]
        domain = config("DOMAIN_NAME")

        # Check whether the specified path exists or not
        isExist = os.path.exists(project)
        if not isExist:
            # Create a new directory because it does not exist
            os.mkdir(project)

            # create a new notebook file
            with open(f"{project}/{file}.ipynb", "w") as notebook:
                pass

            # convert normal file to jupyter notebook file
            FCM().new(path=f"{project}/{file}.ipynb")

            notebook_url = f"{domain}/tree/{project}/{file}.ipynb"
            self.write({"notebook_url": notebook_url})
        else:

            # create a new notebook file
            with open(f"{project}/{file}.ipynb", "w") as notebook:
                pass

            # convert normal file to jupyter notebook file
            FCM().new(path=f"{project}/{file}.ipynb")

            notebook_url = f"{domain}/tree/{project}/{file}.ipynb"
            self.write({"notebook_url": notebook_url})


class ProjectNotebookHandler(BaseRequestHandler):
    def get(self, id):
        project_uid = id
        notebooks = os.listdir(f"{project_uid}")
        domain = config("DOMAIN_NAME")

        notebooks_paths = [
            f"{domain}/tree/{project_uid}/{notebook}"
            for notebook in notebooks
            if notebook.endswith(".ipynb")
        ]
        self.write({"notebooks": notebooks_paths})


def routes():
    return tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/new/notebook/", JupyterNotebookHandler),
            (r"/projects/(?P<id>[0-9\w]+)/notebooks/", ProjectNotebookHandler),
        ],
        autoreload=True,
    )


if __name__ == "__main__":
    app = routes()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()

