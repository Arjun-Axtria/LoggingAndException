"""
This file handles the exception of application
"""

import sys
import logging
from django.http import JsonResponse
from rest_framework.views import exception_handler

logger = logging.getLogger("umLogger")

def custom_exception_handler(exc,context):
    '''custom exception handling function'''
    logger.info(f'start custom_exception_handler')
    handlers={
        'ValidationError': _handle_validation_error,
        'PermissionDenied': _handle_permission_error,
        'AuthenticationFailed': _handle_authentication_error,
        'ObjectDoesNotExist': _handle_object_dne_error,
        'EmptyResultSet': _handle_empty_result_error,
        'FieldDoesNotExist': _handle_field_dne_error,
        'ViewDoesNotExist': _handle_view_dne_error,
        'FieldError': _handle_field_error,
        'BadRequest': _handle_bad_request,
    }
    response = exception_handler(exc,context)
    if response is not None:
        response.data['status_code']=response.status_code
    exception_class = exc.__class__.__name__
    print('exception class',exc,exception_class)
    if exception_class in handlers:
        logger.error(f'exception_class in handler : {exception_class} {exc}')
        return handlers[exception_class](exc,context,response)
    return response

def _handle_authentication_error(exc,context,response):
    """Function handles authentication error of app and return proper message"""
    print('inside handle authentication tokem',exc,type(exc))
    if (str(exc) =="access_token expired"):# pragma: no cover

        response.data = {
            'detail': 'access_token expired',
        }
        response.status_code = 403

    elif (str(exc) == "User does not exists"):

        response.data={
            'detail':'access_token expired',
        }
        response.status_code = 404
    else:
        response.data={
            'detail':'Token prefix missing',
        }
        response.status_code=401

    return response


def _handle_permission_error(exc,contex,response):# pragma: no cover
    response.data={
        'detail':'You do not have permission to perform this action.'
    }
    return response

def _handle_generic_error(exc,context,response):# pragma: no cover
    logger.info(f'start _handle_generic_error')
    if "detail" in response:
        msg=response.detail
    else:
        msg=response
    response.data={
        'detail':msg,
        'status_code':response.status_code
    }
    logger.info(f'response returned from _handle_generic_error : {response}')
    return response


def _handle_validation_error(exc,context,response):

    """Function handles all the validation error of serializer and return proper message"""
    logger.info(f'start _handle_validation_error')
    customized_response = {}
    customized_response['detail'] = []
    for key, value in response.data.items():
        if key !='status_code':
            error = {'field': key, 'error': value}
            customized_response['detail'].append(error)
    customized_response['status_code']=400
    response.data = customized_response
    logger.info(f'response returned from _handle_validation_error : {response}')
    return response


def _handle_object_dne_error(exc, context,response):
    response.data['detail'] = 'Object Does Not Exist'
    response.data['status_code'] = 404
    response.status_code = 404
    return response


def _handle_empty_result_error(exc, context, response):

    response.data['status_code'] = 500
    response.status_code = 500
    return response


def _handle_field_dne_error(exc, context, response):
    response.data['detail'] = 'The requested model field does not exist'
    response.data['status_code'] = 404
    response.status_code = 404
    return response


def _handle_view_dne_error(exc, context, response):
    response.data['detail'] = 'The requested view does not exist'
    response.data['status_code'] = 404
    response.status_code = 404
    return response


def _handle_field_error(exc, context, response):

    response.data['status_code'] = 500
    response.status_code = 500
    return response


def _handle_bad_request(exc, context,response):
    response.data['detail'] = 'Bad Request'
    response.data['status_code'] = 400
    response.status_code = 400
    return response


def error_404(request,exception):

    """Function  handles 404 end point not found error and return proper messsage """
    message=('The endpoint is not found')
    response=JsonResponse(data={'detail':message,'status_code':404})
    response.status_code=404
    logger.info(f'404 response : {response}')
    return response

def error_500(request,exception=None):

    """Function handles all the 500 Internal server error of the application and returns
    proper message"""

    type, value, traceback = sys.exc_info()
    print('Error :', str(value))
    if type.__name__=='DoesNotExist':
        response=JsonResponse(data={'detail':str(value),'status_code':404})
        response.status_code=404
    elif ('missing' in str(value) and type.__name__=='TypeError'):
        response=JsonResponse(data={'detail':str(value),'status_code':404})
        response.status_code=404
    else:
        response=JsonResponse(data={'detail':str(value),'status_code':500})
        response.status_code=500
    return response
