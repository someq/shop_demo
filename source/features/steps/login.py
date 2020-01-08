from behave import given, when, then, step
from time import sleep


@given('Я открыл страницу "Входа"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/login/')


@step('Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element_by_name(name).send_keys(text)


@when('Я отправляю форму')
def submit_form(context):
    context.browser.find_element_by_css_selector('button[type="submit"]').click()


@then('Я должен быть на главной странице')
def should_be_at_main(context):
    assert context.browser.current_url == 'http://localhost:8000/'


@then("Я должен быть на странице входа")
def should_be_at_login(context):
    assert context.browser.current_url.split('?')[0] == 'http://localhost:8000/accounts/login/'


@then('Я должен видеть сообщение об ошибке с текстом "{text}"')
def see_error_with_text(context, text):
    error = context.browser.find_element_by_css_selector('.text-danger')
    assert error.text == text


@then('Я должен видеть ссылку на личный кабинет пользователя "{username}"')
def see_cabinet_link(context, username):
    links = context.browser.find_elements_by_xpath(f'//a[normalize-space()="Привет, {username}!"]')
    assert len(links) == 1, f"На странице должна быть ссылка \"Привет, {username}!\""
