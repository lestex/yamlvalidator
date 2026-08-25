from typer.testing import CliRunner

from yamlvalidator.main import app

runner = CliRunner(env={'TERM': 'dumb'})


def test_cli_bad_type():
    """Run CLI with bad type passed in"""
    result = runner.invoke(app, ['--type', 'buckets'])
    assert result.exit_code == 2
    assert "Invalid value for '--type': 'buckets' is wrong" in result.stdout


def test_cli_bad_config():
    """Run CLI with non-existent config file"""
    result = runner.invoke(app, ['--type', 'bucket', '--config', '.wrong.yml'])
    assert result.exit_code == 2
    assert "Invalid value for '--config': File:" in result.stdout


def test_cli_with_params_set_config(
    config_file_cli_params_set, membership_cache
):
    """Run CLI --show-config option and other valid params"""
    result = runner.invoke(
        app,
        [
            '--type',
            'role',
            '--config',
            config_file_cli_params_set,
            '--skip-group-check',
            '--skip-team-labels-check',
            '--skip-service-account-check',
            '--show-config',
        ],
    )
    assert result.exit_code == 0
    assert (
        '"allowed_types": ["user", "serviceAccount", "group"]' in result.stdout
    )
    assert '"skip_group_check": true' in result.stdout
    assert '"skip_service_account_check": true' in result.stdout
    assert '"skip_team_labels_check": true' in result.stdout
    assert '"cache_file": ".membership_cache"' in result.stdout


def test_cli_with_params_not_set_config(
    config_file_cli_params_not_set, membership_cache
):
    """Run CLI --show-config option and other valid params"""
    result = runner.invoke(
        app,
        [
            '--type',
            'role',
            '--config',
            config_file_cli_params_not_set,
            '--skip-group-check',
            '--skip-service-account-check',
            '--skip-team-labels-check',
            '--show-config',
        ],
    )
    assert result.exit_code == 0
    assert (
        '"allowed_types": ["user", "serviceAccount", "group"]' in result.stdout
    )
    assert '"skip_group_check": true' in result.stdout
    assert '"skip_service_account_check": true' in result.stdout
    assert '"skip_team_labels_check": true' in result.stdout


def test_cli_config_file_skips_survive_unpassed_flags(
    config_file_skips_enabled, membership_cache
):
    """A skip set only in the config file must reach the runtime config.

    The --skip-* flags are not passed here, so nothing may overwrite them.
    """
    _ = membership_cache
    result = runner.invoke(
        app,
        [
            '--type',
            'role',
            '--config',
            config_file_skips_enabled,
            '--show-config',
        ],
    )

    assert '"skip_group_check": true' in result.stdout
    assert '"skip_service_account_check": true' in result.stdout
    assert '"skip_team_labels_check": true' in result.stdout


def test_cli_flag_overrides_config_file(
    config_file_skips_enabled, membership_cache
):
    """A passed flag wins over the config file."""
    _ = membership_cache
    result = runner.invoke(
        app,
        [
            '--type',
            'role',
            '--config',
            config_file_skips_enabled,
            '--no-skip-group-check',
            '--show-config',
        ],
    )

    assert '"skip_group_check": false' in result.stdout
    assert '"skip_team_labels_check": true' in result.stdout


def test_cli_invalid_bucket(
    config_file, invalid_bucket_file, membership_cache
):
    """Run CLI --show-config option and other valid params"""
    _ = invalid_bucket_file, membership_cache
    result = runner.invoke(app, ['--type', 'bucket', '--config', config_file])

    errors_output = ''.join(
        [
            "Error:testbucket::'team' must be set\n",
            'Error:testbucket::filename must be: testbucket_bucket.yml\n',
        ]
    )
    assert result.exit_code == 1
    assert result.stdout == errors_output


def test_cli_no_cache_file_needed_when_group_check_skipped(
    config_file_skips_enabled,
):
    """The cache is only read by the group check, so skipping it must
    not require the cache file to exist."""
    result = runner.invoke(
        app,
        [
            '--type',
            'role',
            '--config',
            config_file_skips_enabled,
            '--cache-file',
            '.does_not_exist',
            '--show-config',
        ],
    )

    assert result.exit_code == 0
    assert 'does not exist' not in result.stdout


def test_cli_cache_file_required_when_group_check_runs(config_file):
    """With the group check on, a missing cache file is a usage error."""
    result = runner.invoke(
        app,
        [
            '--type',
            'role',
            '--config',
            config_file,
            '--cache-file',
            '.does_not_exist',
        ],
    )

    assert result.exit_code == 2
    assert 'does not exist' in result.stdout


def test_cli_malformed_yaml_file(
    config_file, malformed_bucket_file, membership_cache
):
    """A bad file must be reported by name, not raise a traceback."""
    _ = malformed_bucket_file, membership_cache
    result = runner.invoke(app, ['--type', 'bucket', '--config', config_file])

    # a clean exit, not an AttributeError escaping read_file
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 1
    assert 'malformed_bucket.yml' in result.stdout
    assert 'must contain a mapping of resources' in result.stdout


def test_cli_valid_role(config_file, valid_role_file, membership_cache):
    """Run CLI with valid role"""
    _ = valid_role_file, membership_cache
    result = runner.invoke(
        app, ['--type', 'role', '--skip-group-check', '--config', config_file]
    )

    assert result.exit_code == 0
    assert result.stdout == ''
