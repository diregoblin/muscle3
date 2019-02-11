from typing import Optional

from libmuscle.configuration import (Configuration, ParameterValue,
                                     has_parameter_type)

from ymmsl import Reference


class ConfigurationStore:
    """Stores the current configuration for a compute element instance.
    """
    def __init__(self) -> None:
        """Create a ConfigurationStore.

        Initialises the base and overlay layers to an empty
        Configuration.

        A ConfigurationStore has two layers of configuration, a base
        layer that contains an immutable set of parameters set in the
        simulation's configuration, and an overlay layer that holds
        parameter values that have been set at run-time.

        Attributes:
            base: The base layer.
            overlay: The overlay layer.
        """
        self.base = Configuration()
        self.overlay = Configuration()

    def get_parameter(self, name: Reference,
                      typ: Optional[str] = None) -> ParameterValue:
        """Returns the value of a parameter.

        Args:
            name: The name of the parameter to get the value of.
            typ: An optional type designation; if specified the type
                    is checked for a match before returning. Valid
                    values are 'str', 'int', 'float', 'bool',
                    '[float]' and '[[float]]'.

        Raises:
            KeyError: If the parameter has not been set.
            TypeError: If the parameter was set to a value that does
                    not match `typ`.
            ValueError: If an invalid value was specified for `typ`
        """
        if name in self.overlay:
            value = self.overlay[name]
        else:
            value = self.base[name]
        if typ is not None:
            if not has_parameter_type(value, typ):
                raise TypeError('Value for parameter {} is of type {},'
                                ' where a {} was expected.'.format(
                                    name, type(value), typ))
        return value
