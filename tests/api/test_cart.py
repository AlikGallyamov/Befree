import allure
from jsonschema import validate

from befree_tests.api.objects_api import ObjectsApi
from befree_tests.helpers.get_schemas import get_json_schemas
from befree_tests.data.user_item_data import card_jacket, card_bomber_jacket


def test_add_product(get_token, post_remove_jacket_from_cart):
    token = get_token
    objects_api = ObjectsApi()

    response = objects_api.add_product_to_cart(token, card_jacket.product_variation_id_in_card)

    with allure.step('Проверяем статус'):
        assert response.status_code == 200
    with allure.step('Проверяем на соответствие json схеме'):
        validate(response.json(), get_json_schemas("add_product_to_cart_schemas"))
    with allure.step('Проверяем, что товар добавился'):
        assert objects_api.item_in_cart(token, card_jacket.product_variation_id_in_card) is not None


def test_remove_product(get_token, add_bomber_jacket_to_cart):
    token = get_token
    objects_api = ObjectsApi()

    response = objects_api.remove_item_from_cart(token, card_bomber_jacket.product_variation_id_in_catalog)

    with allure.step('Проверяем статус'):
        assert response.status_code == 200
    with allure.step('Проверяем, что товар не приходит в ответе'):
        assert objects_api.item_in_cart(token, card_bomber_jacket.product_variation_id_in_card) is None
