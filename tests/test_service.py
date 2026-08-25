import pytest

from yamlvalidator.config import get_config
from yamlvalidator.entities import get_entity
from yamlvalidator.validators.service import ServiceValidator


def test_service_fields():
    type_ = 'service'
    service = get_entity(type_)()

    assert 'valid_fields' and 'class_name' in dir(service)

    valid_service_fields = [
        'name',
        'service',
        'disable_on_destroy',
    ]

    assert service.valid_fields == valid_service_fields
    assert service.class_name == 'service'


service_test_data = [
    # each tuple represents a test case
    (
        # valid service and valid key
        {
            'service': 'compute.googleapis.com',
        },
        # obj_name
        'compute_googleapis_com',
        # filename
        'apis_service.yml',
        # validation result
        [],
    ),
    (
        # valid service and invalid key
        {
            'service': 'compute.googleapis.com',
        },
        # obj_name
        'compute1_googleapis_com',
        # filename
        'apis_service.yml',
        # validation result
        [
            "'compute1_googleapis_com' is incorrect, "
            'must be: compute_googleapis_com'
        ],
    ),
    (
        # invalid service wrong filename
        {
            'service': 'compute.googleapis.com',
        },
        # obj_name
        'compute_googleapis_com',
        # filename
        'apis1_service.yml',
        # validation result
        [
            "filename 'apis1_service.yml' is incorrect, "
            'must be: apis_service.yml'
        ],
    ),
    (
        # invalid service no `service` field
        {},
        # obj_name
        'compute_googleapis_com',
        # filename
        'apis_service.yml',
        # validation result
        [
            "'service' must be set",
        ],
    ),
    (
        # invalid service no `disable_on_destroy` field
        {
            'service': 'compute.googleapis.com',
            'disable_on_destroy': 'wrong',
        },
        # obj_name
        'compute_googleapis_com',
        # filename
        'apis_service.yml',
        # validation result
        [
            "'disable_on_destroy' must be bool ['false' "
            'is default and can be omitted]'
        ],
    ),
    (
        # invalid service non existent service
        {
            'service': 'compute1.googleapis.com',
        },
        # obj_name
        'compute1_googleapis_com',
        # filename
        'apis_service.yml',
        # validation result
        [],
    ),
    (
        # invalid service disable on destroy
        {'service': 'compute1.googleapis.com', 'disable_on_destroy': 'wrong'},
        # obj_name
        'compute1_googleapis_com',
        # filename
        'apis_service.yml',
        # validation result
        [
            "'disable_on_destroy' must be bool ['false' "
            'is default and can be omitted]'
        ],
    ),
]


@pytest.mark.parametrize(
    'test_input,obj_name,filename,expected', service_test_data
)
def test_service(test_input, obj_name, filename, expected, config_file):
    type_ = 'service'
    validator = ServiceValidator()

    service = get_entity(type_)(**test_input)
    cfg = get_config(config_file)
    cfg.update('obj_name', obj_name)
    cfg.update('filename', filename)

    validator.validate(service, cfg)

    assert sorted(validator.errors) == sorted(expected)
    validator.clear()
