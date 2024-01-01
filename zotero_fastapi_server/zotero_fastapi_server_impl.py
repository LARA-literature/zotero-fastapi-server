"""_____________________________________________________________________

:PROJECT: Zotero FastAPI Server

* Main module implementation *

:details:  Main module implementation.

.. note:: -
.. todo:: - 
________________________________________________________________________
"""


import logging

from zotero_fastapi_server.zotero_fastapi_server_interface import GreeterInterface

class HelloWorld(GreeterInterface):
    def __init__(self) -> None:
        """Implementation of the GreeterInterface
        """
        
    def greet_the_world(self, name: str) -> str:
        """greeting module - adds a name to a greeting

        :param name: person to greet
        :type name: str
        """
        logging.debug(f"Greeting: {name}")
        return f"Hello world, {name} !"        

