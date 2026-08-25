# yamlvalidator

Validate yaml based resources.

`yamlvalidator` parses YAML resource definitions into entity objects and runs
per-entity validators against them, reporting the errors it finds.

## Status

Early development. The entity and validator base classes are in place; concrete
entities, validators and the CLI are still being added.

## Requirements

- Python >= 3.10
Validate YAML resource definitions before they are turned into infrastructure.

`yamlvalidator` reads YAML files describing GCP resources — buckets, secrets,
IAM roles, service accounts, KMS keyrings and keys, BigQuery datasets and
tables, enabled services — and checks them against a set of rules: required
fields, naming and file layout conventions, unknown fields, duplicate entries,
and the shape of IAM permission members. It is meant to run in CI so that a
malformed resource definition fails the pull request instead of the apply.

## Install

```sh
pip install .
```

For development:

```sh
pip install -e '.[dev]'
```

## Usage

```sh
yamlvalidator --help
```

## Development

```sh
make test
```

## Usage

```sh
yamlvalidator --type bucket --config .yamlvalidator.yml
```

Every file in the working directory named `<name>_<type>.yml` is validated,
and the name must match exactly: `myname_bucket.yml` for a bucket called
`myname`. The command exits non-zero and prints one line per problem:

```
Error:my-bucket:Team must be set
Error:my-bucket:filename must be: my-bucket_bucket.yml
```

```
Options:
  --type TEXT                   Type of resource to validate: bqdataset,
                                bqtable, bucket, key, keyring, role, sa,
                                secret, service  [required]
  --config PATH                 Config file location  [default: .yamlvalidator.yml]
  --cache-file PATH             Group membership cache  [default: .membership_cache]
  --skip-team-labels-check / --no-skip-team-labels-check
                                Skip the team name check
  --skip-group-check / --no-skip-group-check
                                Skip the group existence check
  --skip-service-account-check / --no-skip-service-account-check
                                Skip the service account existence check
  --show-config                 Print the effective configuration
  --help                        Show this message and exit
```

## Configuration

Policy is configuration, not code. See [`.yamlvalidator.yml`](.yamlvalidator.yml)
for a documented example. The main options:

| Option | Meaning |
| --- | --- |
| `allowed_types` | Member types accepted in permissions (`user`, `group`, `serviceAccount`) |
| `allowed_group_domains` | Domains a group may belong to; empty disables the check |
| `allowed_user_domains` | Domains an individual user may belong to; empty disables the check |
| `allowed_user_emails` | Individual users allowed as an exception |
| `sa_project_prefix` | Service accounts in projects with this prefix are checked for existence in GCP |
| `sa_id_substring` | Substring every `account_id` must contain; empty disables the check |
| `allowed_service_accounts` | Service accounts exempt from `sa_id_substring` |
| `team_validation_url` | Optional endpoint used to verify a resource's `team`; unset disables the check |

The `--skip-*` flags disable the checks that talk to GCP or to the network,
which is what you want when running locally or in a test.

### The group membership cache

`--cache-file` is a YAML mapping of group emails that are known to exist.
The tool only ever reads it — it is populated out-of-band — and it is read
once per run. It is required only when the group check will actually run,
so `--skip-group-check` needs no cache file present.

### Precedence

**A `--skip-*` flag wins when it is passed; otherwise the config file value
stands, and its default if the file does not set it.** Pass `--no-skip-...`
to force a check back on from the command line when the config file disables
it.

## Adding a resource type

The four layers are independent, so a new resource type is four small files.

1. **Entity** — a `@dataclass` subclass of `BaseYamlEntity` in `src/entities/`
   describing the YAML shape. `name` comes from the base class. To validate
   unknown fields, define `__init__` as:

   ```python
   def __init__(self, **kwargs):
       for k, v in kwargs.items():
           setattr(self, k, v)
   ```

   Register it in the dictionary in `src/entities/__init__.py`.

2. **Rules** — functions in `src/rules/` with the signature:

   ```python
   def validate_name(entity: BaseYamlEntity, config: Config) -> list[str]:
   ```

   Each returns a list of error strings, empty when the entity is valid.
   Common rules live in `src/rules/__init__.py`, permission-specific ones in
   `src/rules/permissions.py`.

3. **Validator** — a `BaseValidator` subclass in `src/validators/` with a
   `checks` dictionary mapping names to rule functions.

4. Register the validator in the dictionary in `src/validators/__init__.py`.

## Development

```sh
pip install -e ".[dev]"
make test        # run the test suite
make coverage    # run with coverage
make lint        # ruff check + format check
make format      # apply formatting
```

## License

MIT - see [LICENSE](LICENSE).
