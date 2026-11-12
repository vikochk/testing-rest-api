from src.models.post_model import PostModel
from src.models.user_model import UserModel
from src.utils.logger import Logger
from src.utils.random_generation import RandomGeneration


class TestRestApi:
    def test_rest_api(self, api_client, posts_data, users_data):
        Logger.info('Загрузка тестовых данных')
        get_all_posts_data = posts_data["get_all_posts"]
        get_post_by_id_data = posts_data["get_existing_post_by_id"]
        get_non_existent_post_data = posts_data["get_non_existent_post"]
        create_post_data = posts_data["create_post"]
        get_all_users_data = users_data["get_all_users"]
        get_user_by_id_data = users_data["get_user_by_id"]

        Logger.info(f'Шаг 1. Получить все сообщения по запросу /posts')
        Logger.info('Проверка кода состояния')
        response = api_client.get_all_posts()
        assert response.status_code == get_all_posts_data.status_code
        
        Logger.info('Проверка типа данных (должен быть список JSON)')
        posts = response.data
        assert isinstance(posts, list), 'Ответ должен быть списком'
        
        Logger.info('Проверка сортировки по id')
        idx_list = [post.id for post in posts]
        assert idx_list == sorted(idx_list), 'Посты не отсортированы по возрастанию id'

        Logger.info(f'Шаг 2. Получить пост с id={get_post_by_id_data.id}')
        Logger.info('Проверка кода состояния')
        response = api_client.get_post_by_id(get_post_by_id_data.id)
        assert response.status_code == get_post_by_id_data.status_code
        
        Logger.info('Автоматическая валидация данных через модель PostModel')
        post = response.data 

        Logger.info('Проверка корректности данных')
        assert post.user_id == get_post_by_id_data.expected_user_id, \
            f'Ожидался userId={get_post_by_id_data.expected_user_id}, получен {post.user_id}'
        assert post.id == get_post_by_id_data.id, f'Ожидался id={get_post_by_id_data.id}, получен {post.id}'
        assert post.title, 'Заголовок не должен быть пустым'
        assert post.body, 'Тело сообщения не должно быть пустым'

        Logger.info(f'Шаг 3. Получить несуществующий пост с id={get_non_existent_post_data.id}')
        Logger.info('Проверка кода состояния')
        response = api_client.get_post_by_id(get_non_existent_post_data.id)
        assert response.status_code == get_non_existent_post_data.status_code
        
        Logger.info('Проверка того, что тело ответа пустое')
        assert response.text == '' or response.text == '{}', 'Тело ответа должно быть пустым'

        Logger.info(f'Шаг 4. Отправить новый пост с userId={create_post_data.expected_user_id} и случайным содержанием')
        Logger.info('Генерация случайного содержания для будущего запроса и отправка на сайт')
        new_data = {
            'userId' : create_post_data.expected_user_id,
            'body' : RandomGeneration.generate_string(),
            'title' : RandomGeneration.generate_string()
        }
        response = api_client.create_post(new_data)
        
        Logger.info('Проверка кода состояния')
        assert response.status_code == create_post_data.status_code
        
        Logger.info('Автоматическая валидация данных через модель PostModel')
        post = response.data
        
        Logger.info('Проверка корректности данных')
        assert post.user_id == create_post_data.expected_user_id, \
            f'Ожидался userId={create_post_data.expected_user_id}, получен {post.user_id}'
        assert post.id, 'id не должен быть пустым'
        assert post.title == new_data.get('title'), \
            f'Заголовок полученного сообщения ({post.title}) не совпадает с ожидаемым ({new_data.get("title")})'
        assert post.body == new_data.get('body'), \
            f'Тело полученного сообщения ({post.body}) не совпадает с ожидаемым ({new_data.get("body")})'

        Logger.info('Шаг 5. Получить всех пользователей')
        Logger.info('Проверка кода состояния')
        response = api_client.get_all_users()
        assert response.status_code == get_all_users_data.status_code
        
        Logger.info('Проверка типа данных (должен быть список JSON)')
        users = response.data
        assert isinstance(users, list), 'Ответ должен быть списком'

        Logger.info(f'Проверка данных пользователя с id={get_all_users_data.expected_user_id}')
        test_user_data = next((user for user in users if user.id == get_all_users_data.expected_user_id), None)
        required_user_data = get_all_users_data.expected_data
        assert required_user_data == test_user_data, 'Данные пользователя с сайта и ожидаемые не совпали'
    
        Logger.info(f'Шаг 6. Получить пользователя с id={get_user_by_id_data.expected_user_id}')
        Logger.info('Проверка кода состояния')
        response = api_client.get_user_by_id(get_user_by_id_data.expected_user_id)
        assert response.status_code == get_user_by_id_data.status_code

        Logger.info('Автоматическая валидация данных через модель UserModel')
        user_data = response.data

        Logger.info(f'Проверка данных пользователя с id={get_user_by_id_data.expected_user_id}')
        assert required_user_data == user_data, 'Данные пользователя с сайта и ожидаемые не совпали'