"""
Base model for Incus resources.
"""

from typing import Dict, Any, Optional


class Model:
    """Base model for Incus resources."""

    def __init__(self, client=None, **kwargs):
        """
        Initialize a new model instance.

        Args:
            client: The Incus client instance.
            **kwargs: Additional attributes to set on the model.
        """
        self._client = client
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """Return a string representation of the model."""
        return f"<{self.__class__.__name__}>"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary.

        Returns:
            Dict[str, Any]: The model as a dictionary.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client=None) -> "Model":
        """
        Create a model instance from a dictionary.

        Args:
            data: The dictionary containing the model data.
            client: The Incus client instance.

        Returns:
            Model: A new model instance.
        """
        return cls(client=client, **data)
