import datetime as dt
import typing as tp

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from . import crud
from . import serializers


class RefbooksApiView(APIView):
    http_method_names = ['get']
    
    def get(self, request: Request):
        date = request.query_params.get('date', None)
        
        if date is None:
            refbooks_list = crud.get_all_refbooks()
        elif self._validate_date(date):
            refbooks_list = crud.get_refbooks_actual_by_date(date)
        else:
            return Response({'msg': 'date must have YYYY-MM-DD format'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        response_data = {'refbooks': refbooks_list}
        serializer = serializers.RefbooksResponseSerializer(response_data)
        return Response(serializer.data)

    @staticmethod
    def _validate_date(date: str):
        try: 
            dt.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return False
        return True


class RefbooksElementsApiView(APIView):
    http_method_names = ['get']
    
    def get(self, request: Request, id: int):
        version = request.query_params.get('version', None)
        refbook_elements_list = self._get_refbook_elements_list(id, version)
        response_data = {'elements': refbook_elements_list}
        serializer = serializers.RefbooksElementsResponseSerializer(response_data)
        return Response(serializer.data)
    
    @staticmethod
    def _get_refbook_elements_list(id: int, version: tp.Optional[str]):
        if version is not None:
            return crud.get_refbook_elements_for_version(id, version)
            
        have_any_versions = crud.check_any_refbook_version_exists(id)
        if not have_any_versions:
            return []
        
        version = crud.get_current_refbook_version(id).version
        return crud.get_refbook_elements_for_version(id, version)


class CheckRefbookElementApiView(APIView):
    http_method_names = ['get']
    
    def get(self, request: Request, id: int):
        code = request.query_params.get('code', None)
        value = request.query_params.get('value', None)
        version = request.query_params.get('version', None)
        
        if code is None or value is None:
            return Response({'msg': "'code' and 'value' query params are required"}, 
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if version is None:
            version = crud.get_current_refbook_version(id).version
        
        is_exists = crud.check_refbook_element_exists(code, value, version)
        return Response(is_exists)
