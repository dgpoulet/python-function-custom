import logging

import azure.functions as func
from davpopackage import davpo_module


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger v1 function processed a request.')

    name = req.params.get('name')
    mynumber = davpo_module.return_fortytwo()

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Getting number {mynumber}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
