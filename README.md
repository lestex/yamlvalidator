# yamlvalidator

Validate yaml based resources.

`yamlvalidator` parses YAML resource definitions into entity objects and runs
per-entity validators against them, reporting the errors it finds.

## Status

Early development. The entity and validator base classes are in place; concrete
entities, validators and the CLI are still being added.

## Requirements

- Python >= 3.10

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

## License

MIT - see [LICENSE](LICENSE).
