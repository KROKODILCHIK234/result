from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import sys

sys.path.append(os.path.join(Path(__file__).parent, 'src'))

from error_proxy import error_proxy
from pathlib import Path

from storage.storage import storage
from src.Logic.Reporting.Json_convert.reference_conventor import reference_conventor
from exceptions import argument_exception
from src.Logic.storage_observer import storage_observer
from src.models.event_type import event_type
from src.models.log_type_model import log_type

# для референсов
from src.storage.storage_turn_model import storage_turn_model
from models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.nomenclature_group_model import nomenclature_group_model
from storage.storage_journal_row import storage_journal_row
from src.Logic.services.abstract_service import abstract_sevice
from src.Logic.services.post_processing_sevice import post_processing_service


# PERENESTI I ZAMENIT MAIN

class nomenclature_service(abstract_sevice):

    # конструктор
    def __init__(self, data: list):

        if len(data) == 0:
            raise argument_exception("Wrong argument")

        self.__data = data

    # возвращаем массив с добавленной номенклатурой
    def add_nom(self, nom: nomenclature_model):
        storage_observer.raise_event(event_type.make_log(log_type.log_type_debug(), "добавление номенклатуры",
                                                         "nomenclature_service.py/add_nom"))
        self.__data.append(nom)
        return self.__data

    # ищем номенклатуру и меняем её
    def change_nome(self, nom: nomenclature_model):
        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == nom.id:
                self.__data[index] = nom
                break
        storage_observer.raise_event(event_type.make_log(log_type.log_type_debug(), "изменение номенклатуры",
                                                         "nomenclature_service.py/change_nome"))
        return self.__data

    # ищем по айди и передаём
    # Если в api была передана конкретная id, то мы ищем её, преобразуем в json и возвращаем
    def get_nom(self, id: uuid.UUID):
        # при разных типах данных hash возвращает разные коды, поэтому переводим id в uuid и сравениваем
        id = uuid.UUID(id)

        for cur_nom in self.__data:
            if id == cur_nom.id:
                reference = reference_conventor(nomenclature_model,
                                                error_proxy,
                                                nomenclature_group_model,
                                                range_model,
                                                storage_journal_row,
                                                storage_turn_model)
                storage_observer.raise_event(event_type.make_log(log_type.log_type_debug(), "получение номенклатуры",
                                                                 "nomenclature_service.py/get_nom"))
                return cur_nom

    # ищем по айди, удаляем, возвращаем массив
    def delete_nom(self, id: str):
        # при разных типах данных hash возвращает разные коды, поэтому переводим id в uuid и сравениваем
        id = uuid.UUID(id)
        res = False

        # obs=post_processing_service()
        # obs.nomenclature_id=id

        for index, cur_nom in enumerate(self.__data):
            if cur_nom.id == id:
                self.__data.pop(index)
                res = True
                # если функция удаления нашла номенклатуру, то сразу жу вызываем наблюдателя
                storage_observer.raise_event(event_type.make_log(log_type.log_type_debug(), "удаление номенклатуры",
                                                                 "nomenclature_service.py/delete_nom"))
                storage_observer.raise_event(event_type.deleted_nomenclature_id(id))
                break
        return self.__data, res

    @staticmethod
    def create_response(data: dict, app):

        if app is None:
            raise argument_exception()
        json_text = json.dumps(data)

        # Подготовить ответ
        result = app.response_class(
            response=f"{json_text}",
            status=200,
            mimetype="application/json; charset=utf-8"
        )

        return result
