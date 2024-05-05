from Src.Models.log_type_model import log_type_model
from Src.Logics.Services.post_processing_service import post_processing_service
from Src.Models.event_type import event_type
from Src.Logics.Services.service import service
from Src.exceptions import exception_proxy, operation_exception
from Src.reference import reference
from Src.Logics.storage_observer import storage_observer

#
# Сервис для выполнения CRUD операций
#
class reference_service(service):

    def __init__(self, data: list) -> None:
        super().__init__(data)
        storage_observer.observers.append(self)
        
    def add(self, item: reference) -> bool:
        """
            Добавить новый элемент
        """
        exception_proxy.validate(item, reference)
        found = list(filter(lambda x: x.id == item.id , self.data))     
        if len(found) > 0:
            return False
        
        self.data.append(item)
        storage_observer.raise_event(event_type.make_log(log_type_model.log_type_debug(), "Добавлен новый элемент", "reference_service.py/add"))
        return True
    
    def delete(self, item:reference) -> bool:
        """
            Удалить элемент
        """
        exception_proxy.validate(item, reference)
        found = list(filter(lambda x: x.id == item.id , self.data))     
        if len(found) == 0:
            return False
        
        self.data.remove(found[0])
        storage_observer.raise_event(event_type.make_log(log_type_model.log_type_debug(), "Удалён элемент", "reference_service.py/delete"))
        return True

    def change(self, item:reference) -> bool:
        """
            Изменить элемент
        """
        exception_proxy.validate(item, reference)
        found = list(filter(lambda x: x.id == item.id , self.data))     
        if len(found) == 0:
            return False
        
        self.delete(found[0])
        self.add(item)
        storage_observer.raise_event(event_type.make_log(log_type_model.log_type_debug(), "Изменён элемент", "reference_service.py/change"))
        return True
    
    def get(self) -> list:
        """
            Вернуть список 
        """
        return self.data
    
    def get_item(self, id: str) -> reference:
        """
            Вернуть элемент
        """
        exception_proxy.validate(id, str)
        found = list(filter(lambda x: x.id == id , self.data))     
        if len(found) == 0:
            raise operation_exception(f"Не найден элемент с кодом {id}!")
        
        return found
    
    def handle_event(self, handle_type: str):
        """
            Обработать событие
        Args:
            handle_type (str): _description_
        """
        super().handle_event(handle_type)
