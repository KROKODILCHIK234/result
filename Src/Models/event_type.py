from Src.reference import reference


#
# Типы событий
#
class event_type(reference):

    @staticmethod
    def changed_block_period() -> str:
        """
            Событие изменения даты блокировки
        Returns:
            str: _description_
        """
        return "changed_block_period"

    @staticmethod
    def deleted_nomenclature() -> str:
        """
            Событие о удалении номенклатуры
        Returns:
            str: _description_
        """
        return f"deleted_nomenclature {str(id)}"

    @staticmethod
    def make_log_key():
        return f"make_log"

    @staticmethod
    def make_log(type: str, text: str, source: str):
        return f"make_log {type} {text} {source}"