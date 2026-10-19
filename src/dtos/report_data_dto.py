class report_data_dto:
    """
    DTO для передачи табличных данных между моделями и отчетами.
    Применяется для отделения структуры данных от логики их формирования (DDD).
    """
    def __init__(
        self,
        title: str = "",
        headers: list = None,
        rows: list = None,
        footer: str = ""
    ):
        self.title = title
        self.headers = headers or []
        self.rows = rows or []
        self.footer = footer