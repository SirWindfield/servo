# META: timeout=long

import base64
import imghdr

import pytest

from tests.support.asserts import assert_success
from tests.support.inline import inline


def take_element_screenshot(session, element_id):
    return session.transport.send(
        "GET",
        "session/{session_id}/element/{element_id}/screenshot".format(
            session_id=session.session_id,
            element_id=element_id,
        )
    )


@pytest.fixture
def check_user_prompt_not_closed_without_exception(session, create_dialog):
    def check_user_prompt_not_closed_without_exception(dialog_type):
        session.url = inline("<input/>")
        element = session.find.css("input", all=False)

        create_dialog(dialog_type, text=dialog_type)

        response = take_element_screenshot(session, element.id)
        value = assert_success(response)

        image = base64.decodestring(value)
        assert imghdr.what("", image) == "png"

        assert session.alert.text == dialog_type
        session.alert.dismiss()

    return check_user_prompt_not_closed_without_exception


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_accept(check_user_prompt_not_closed_without_exception, dialog_type):
    check_user_prompt_not_closed_without_exception(dialog_type)


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept and notify"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_accept_and_notify(check_user_prompt_not_closed_without_exception, dialog_type):
    check_user_prompt_not_closed_without_exception(dialog_type)


@pytest.mark.capabilities({"unhandledPromptBehavior": "dismiss"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_dismiss(check_user_prompt_not_closed_without_exception, dialog_type):
    check_user_prompt_not_closed_without_exception(dialog_type)


@pytest.mark.capabilities({"unhandledPromptBehavior": "dismiss and notify"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_dismiss_and_notify(check_user_prompt_not_closed_without_exception, dialog_type):
    check_user_prompt_not_closed_without_exception(dialog_type)


@pytest.mark.capabilities({"unhandledPromptBehavior": "ignore"})
@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_ignore(check_user_prompt_not_closed_without_exception, dialog_type):
    check_user_prompt_not_closed_without_exception(dialog_type)


@pytest.mark.parametrize("dialog_type", ["alert", "confirm", "prompt"])
def test_default(check_user_prompt_not_closed_without_exception, dialog_type):
    check_user_prompt_not_closed_without_exception(dialog_type)
