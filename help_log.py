import logging
import threading
import uuid
import requests



# # developers will need to add the decorator to the dipatch function in their API view class
# # if there is no dispatch function, they will need to add it
# # for example:
# @help_log.add_uuid_to_dispatch
# def dispatch(self, request, *args, **kwargs):
#     return super().dispatch(request, *args, **kwargs)
def add_uuid_to_dispatch(func):
    def wrapper(self, request, *args, **kwargs):
        axtria_uuid = request.headers.get('X-Axtria-UUID')
        if(axtria_uuid == None):
            axtria_uuid = str(uuid.uuid4())
        threading.current_thread().uuid = axtria_uuid

        return func(self, request, *args, **kwargs)
    return wrapper



# # developers can either add the following line before the APIView class
# requests = help_log.CustomSession() 
# # or they can change 
# # requests.get = help_log.CustomSession().get etc.
class RequestSession(requests.Session):
    def get(self, url, **kwargs):
        # Modify the headers to include UUID
        kwargs = self._update_kwargs(**kwargs)

        # Call the original get method from the parent class
        return super().get(url, **kwargs)


    def head(self, url, **kwargs):
        # Modify the headers to include UUID
        kwargs = self._update_kwargs(**kwargs)

        # Call the original head method from the parent class
        return super().head(url, **kwargs)


    def post(self, url, data=None, json=None, **kwargs):
        # Modify the headers to include UUID
        kwargs = self._update_kwargs(**kwargs)

        # Call the original post method from the parent class
        return super().post(url, data=data, json=json, **kwargs)


    def put(self, url, data=None, **kwargs):
        # Modify the headers to include UUID
        kwargs = self._update_kwargs(**kwargs)

        # Call the original put method from the parent class
        return super().put(url, data=data, **kwargs)


    def patch(self, url, data=None, **kwargs):
        # Modify the headers to include UUID
        kwargs = self._update_kwargs(**kwargs)

        # Call the original patch method from the parent class
        return super().patch(url, data=data, **kwargs)


    def delete(self, url, **kwargs):
        # Modify the headers to include UUID
        kwargs = self._update_kwargs(**kwargs)

        # Call the original delete method from the parent class
        return super().delete(url, **kwargs)


    def _update_kwargs(self, **kwargs):
        try:
            kwargs['headers'].update({'X-Axtria-UUID': threading.current_thread().uuid})
        except:
            try:
                kwargs['headers'] = {'X-Axtria-UUID': threading.current_thread().uuid}
            except:
                pass
        return kwargs



# # developers will need to add the following line
# logger = help_log.CustomLogger(__name__) 
# # where name has to be replaced with the name of the logger in the settings.py file
# |||
# # developers will need to change the settings.py format such that it does not include the filename,
# # funcname and lineno
# # the filename, funcname, lineno and the UUID will be formatted into the message
# the _format_caller_info function changes the message such that it includes the filename funcname and lineno
class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.handlers = logging.getLogger(name).handlers
        self.setLevel(logging.getLogger(name).level)


    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """

        stacklevel += 2
        return super().findCaller(stack_info, stacklevel)


    def debug(self, msg, *args, **kwargs):

        msg = self._update_msg(msg)

        super().debug(msg, *args, **kwargs)


    def info(self, msg, *args, **kwargs):

        msg = self._update_msg(msg)

        super().info(msg, *args, **kwargs)


    def warning(self, msg, *args, **kwargs):

        msg = self._update_msg(msg)

        super().warning(msg, *args, **kwargs)


    def error(self, msg, *args, **kwargs):

        msg = self._update_msg(msg)

        super().error(msg, *args, **kwargs)


    def critical(self, msg, *args, **kwargs):

        msg = self._update_msg(msg)

        super().critical(msg, *args, **kwargs)


    def _update_msg(self, msg):
        try:
            msg = '['+ threading.current_thread().uuid + '] => ' + msg
        except:
            pass
        return msg



def modify_request_session(requests):
    session = RequestSession()
    requests.get = session.get
    requests.post = session.post
    requests.put = session.put
    requests.delete = session.delete
    requests.patch = session.patch
    requests.head = session.head
    return requests