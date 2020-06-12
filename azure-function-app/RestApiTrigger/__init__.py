import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:    
    logging.info(str(req.headers))
    logging.info(str(req.get_body()))
    logging.info(str(req.get_json()))

    return func.HttpResponse(f"Hello!")
