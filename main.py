import json
import datetime
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
        self.set_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
        )

    def options(self):
        self.set_status(204)
        self.finish()


class JupyterNotebookHandler(BaseRequestHandler):
    def post(self):

        try:
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

                notebook_url = f"{domain}/{notebooks_dir}/{project}/{file}.ipynb"
                self.write({"notebook_url": notebook_url})
            else:

                # create a new notebook file
                with open(f"{notebooks_dir}/{project}/{file}.ipynb", "w") as notebook:
                    pass

                # convert normal file to jupyter notebook file
                FCM().new(path=f"{notebooks_dir}/{project}/{file}.ipynb")

                notebook_url = f"{domain}/{notebooks_dir}/{project}/{file}.ipynb"
                self.write({"notebook_url": notebook_url})
        except Exception as e:
            self.write({"error": str(e)})






class ProjectNotebookHandler(BaseRequestHandler):
    def get(self, id):
        try:
            project_uid = id
            notebooks_dir = "notebooks"

            notebooks = os.listdir(f"{notebooks_dir}/{project_uid}")
            domain = config("DOMAIN_NAME")

            notebooks_paths = [
                {
                    "notebook_name": notebook,
                    "created": datetime.datetime.fromtimestamp(
                        os.path.getctime(
                            os.path.abspath(f"{notebooks_dir}/{project_uid}/{notebook}")
                        )
                    ).strftime("%m/%d/%Y %H:%M"),
                    "updated": datetime.datetime.fromtimestamp(
                        os.path.getmtime(
                            os.path.abspath(f"{notebooks_dir}/{project_uid}/{notebook}")
                        )
                    ).strftime("%m/%d/%Y %H:%M"),
                    "notebook_url": f"{domain}/{notebooks_dir}/{project_uid}/{notebook}",
                }
                for notebook in notebooks
                if notebook.endswith(".ipynb")
            ]
            self.write({"notebooks": notebooks_paths})
        except Exception as e:
            self.write({"error": str(e)})




def routes():
    return tornado.web.Application(
        [
            (r"/notes", IndexHandler),
            (r"/new/notebook/", JupyterNotebookHandler),
            (r"/projects/(?P<id>[0-9\w]+)/notebooks/", ProjectNotebookHandler),
        ],
        autoreload=True,
    )


if __name__ == "__main__":
    app = routes()
    app.listen(9000)
    tornado.ioloop.IOLoop.current().start()
