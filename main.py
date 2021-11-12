import json
import os.path, time
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
        self.set_header("Access-Control-Allow-Methods", "DELETE, POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")

    def options(self):
        self.set_status(204)
        self.finish()


class JupyterNotebookHandler(BaseRequestHandler):
    def post(self):

        payload = json.loads(self.request.body)
        project = payload["project"]
        file = payload["notebook_name"]
        domain = config("DOMAIN_NAME")

        notebooks_dir = "notebooks"
    
        # Check whether the specified path exists or not
        isExist = os.path.exists(f"{notebooks_dir}/{project}/")
        if not isExist:
            # Create a new directory because it does not exist
            os.mkdir(f"{notebooks_dir}/{project}/")

            # create a new notebook file
            with open(f"{notebooks_dir}/{project}/{file}.ipynb", "w") as notebook:
                pass

            # convert normal file to jupyter notebook file
            FCM().new(path=f"{notebooks_dir}/{project}/{file}.ipynb")

            notebook_url = f"{domain}/tree/{notebooks_dir}/{project}/{file}.ipynb"
            self.write({"notebook_url": notebook_url})
        else:

            # create a new notebook file
            with open(f"{notebooks_dir}/{project}/{file}.ipynb", "w") as notebook:
                pass

            # convert normal file to jupyter notebook file
            FCM().new(path=f"{notebooks_dir}/{project}/{file}.ipynb")

            notebook_url = f"{domain}/tree/{notebooks_dir}/{project}/{file}.ipynb"
            self.write({"notebook_url": notebook_url})


class ProjectNotebookHandler(BaseRequestHandler):
    def get(self, id):
        project_uid = id
        notebooks_dir = "notebooks"

        notebooks = os.listdir(f"{notebooks_dir}/{project_uid}")
        domain = config("DOMAIN_NAME")
    
        notebooks_paths = [
             {
                "notebook_name": notebook,
                # "created":time.ctime(os.path.getctime({notebooks_dir}/{project_uid}/{notebook})),
                # "updated":time.ctime(os.path.getctime({notebooks_dir}/{project_uid}/{notebook})),
                "notebook_url": f"{domain}/tree/{notebooks_dir}/{project_uid}/{notebook}",
            }
            for notebook in notebooks
            if notebook.endswith(".ipynb")
        ]
        self.write({"notebooks":notebooks_paths})


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

