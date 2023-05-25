import os.path

from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, password_space, email_space

pf = PetFriends()

def test_get_api_key(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) > 0

def test_post_my_pet_with_valid_data(name='Sally', animal_type='кошка',
                                     age='5', pet_photo='images/pet_photo.jpeg'):
    '''Проверяем, что питомца можно добавить с корректными данными'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_my_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_delete_my_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_my_pet(auth_key, "Cэм", "кот", '3', "images/pet_photo1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

     # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_my_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_change_my_pet(name='Billy', animal_type='кот', age='1'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить имя, тип и возраст животного
    if len(my_pets['pets']) > 0:
        status, result = pf.change_my_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_pet_wihtout_photo_with_valid_data(name='Мышка', animal_type='кошка', age=2):
    '''Проверяем, что питомца можно добавить без фото с корректными данными'''

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_for_my_pet_with_valid_data(pet_photo='images/pet_photo2.jpg'):
    '''Проверяем, что к существующей карточке питомца можно добавить фотографию(с корректными данными)'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст животного
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_for_my_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['pet_photo'] != pet_photo
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с некоректными данными(пароль) возвращает статус равный 403
    и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа с некоректными данными(email) возвращает статус равный 403
    и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_email_space(email=email_space, password=valid_password):
    """ Проверяем что запрос api ключа с некоректными данными(графа email оставлен пустым) возвращает статус
    равный 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_password_space(email=valid_email, password=password_space):
    """ Проверяем что запрос api ключа с некоректными данными(графа пароль оставлен пустым) возвращает статус
    равный 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_add_pet_wihtout_photo_with_invalid_age(name='Хося', animal_type='собака', age=-2):
    '''Проверяем, что питомца нельзя добавить без фото с некорректными данными (отрицательный возраст)'''
    """В данном методе присутсвует баг, так животное с отрицательным возрастом добавляется успешно 
    и приходит ответ:200"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] != name

def test_add_pet_wihtout_photo_with_space_data(name='', animal_type='', age=0):
    '''Проверяем, что питомца нельзя добавить без фото с некорректными данными (пустые значения при
    передаче имени и типа животного)'''
    """В данном методе присутсвует баг, так животное без имени и типа добавляется успешно и приходит ответ:200"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] != name


def test_post_my_pet_with_space_data_with_photo(name='', animal_type='',
                                     age='', pet_photo='images/pet_photo1.jpg'):
    '''Проверяем, что питомца нельзя добавить с незаполнеными данными (пустые значения при
    передаче имени, типа животного и возраста) животного, но с фотографией'''
    """В данном методе присутсвует баг, так животное без имени, типа и возраста, но с фотографией, 
        добавляется успешно и приходит ответ:200"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_my_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] != name

def test_change_my_pet_with_space_data(name='', animal_type='', age=''):
    """Проверяем, что при обновлении информации о питомце невозможно заменить данные на пустые значения"""
    """В данном методе присутсвует баг, так как в карточке животного нельзя изменить данные 
        на пустые значения, но статус ответа приходит:200, а не 400"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.change_my_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
        assert status == 400
        assert result['name'] != name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

















