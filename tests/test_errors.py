from src.errors import Errors


def test_errors_add_non_existed():
    errors = Errors()

    assert errors == {}

    errors_name = 'test'
    errors_to_add = ['test_error1', 'test_error2']

    errors.add(errors_name, errors_to_add)

    assert errors != {}
    assert 'test' in errors
    assert errors['test'] == errors_to_add


def test_errors_add_existed():
    errors = Errors()

    errors_name1 = 'test'
    errors_to_add1 = ['test_error1', 'test_error2']

    errors.add(errors_name1, errors_to_add1)
    assert 'test' in errors

    errors_to_add2 = ['test_error3', 'test_error4']
    errors.add(errors_name1, errors_to_add2)

    assert 'test' in errors
    assert errors['test'] == errors_to_add1 + errors_to_add2


def test_errors_add_copies_the_list():
    """A caller must be able to clear its own list after adding it."""
    errors = Errors()

    entity_errors = ['test_error1', 'test_error2']
    errors.add('test', entity_errors)
    entity_errors.clear()

    assert errors['test'] == ['test_error1', 'test_error2']


def test_error_print():
    errors = Errors()

    errors_name1 = 'test'
    errors_to_add1 = ['test_error1', 'test_error2']

    errors.add(errors_name1, errors_to_add1)
    errors_to_add2 = ['test_error3', 'test_error4']
    errors.add(errors_name1, errors_to_add2)

    output_str = """Error:test:test_error1
Error:test:test_error2
Error:test:test_error3
Error:test:test_error4"""

    assert str(errors) == output_str
