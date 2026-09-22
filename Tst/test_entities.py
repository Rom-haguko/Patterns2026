# Необходимо установить pip install pytest в терминале с подключенным Environment
# Далее, настройки
# {
#    "python.testing.pytestArgs": [
#        "Tst"
#    ],
#    "python.testing.unittestEnabled": false,
#    "python.testing.pytestEnabled": true
#}

from src.core.abstract_model import name_id

class test_entity(name_id):
    pass

# Пример простого теста
def abstract_model_get_id_not_null():

    entity = test_entity()

    # Дейтсвие
    result = entity.id

    # Проверка
    assert result != ""



