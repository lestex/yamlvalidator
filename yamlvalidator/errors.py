from collections import UserDict


class Errors(UserDict):
    """Errors dictionary class"""

    def add(self, entity_name: str, entity_errors: list[str]) -> None:
        """Adds entity and its errors to a dict.

        The errors are copied, so the caller is free to reuse or clear
        the list it passed in.
        """
        if entity_name in self.data:
            self.data[entity_name].extend(entity_errors)
        else:
            self.data[entity_name] = list(entity_errors)

    def __str__(self) -> str:
        """Generates string representation of all errors to
        be used by print() function.
        """
        output = []
        for entity_name, entity_errors in self.data.items():
            output.extend(
                [f'Error:{entity_name}:{error}' for error in entity_errors]
            )
        return '\n'.join(output)
