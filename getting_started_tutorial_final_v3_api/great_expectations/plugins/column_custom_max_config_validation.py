# todo(jdimatteo) are these imports needed? also fixed missing except and messed up whitespace
from great_expectations.core import ExpectationConfiguration
from typing import Optional


def validate_configuration(self, configuration: Optional[ExpectationConfiguration]):
   """
   Validates that a configuration has been set, and sets a configuration if it has yet to be set. Ensures that
   necessary configuration arguments have been provided for the validation of the expectation.

   Args:
       configuration (OPTIONAL[ExpectationConfiguration]): \
           An optional Expectation Configuration entry that will be used to configure the expectation
   Returns:
       True if the configuration has been validated successfully. Otherwise, raises an exception
   """
   min_val = None
   max_val = None

   # Setting up a configuration
   super().validate_configuration(configuration)
   if configuration is None:
       configuration = self.configuration

   # Ensuring basic configuration parameters are properly set
   try:
     assert (
         "column" in configuration.kwargs
     ), "'column' parameter is required for column map expectations"
   except AssertionError as e:
     raise InvalidExpectationConfigurationError(str(e))

   # Validating that Minimum and Maximum values are of the proper format and type
   if "min_value" in configuration.kwargs:
     min_val = configuration.kwargs["min_value"]

   if "max_value" in configuration.kwargs:
     max_val = configuration.kwargs["max_value"]

   try:
     # Ensuring Proper interval has been provided
     assert (
         min_val is not None or max_val is not None
     ), "min_value and max_value cannot both be none"
     assert min_val is None or isinstance(
         min_val, (float, int)
     ), "Provided min threshold must be a number"
     assert max_val is None or isinstance(
         max_val, (float, int)
     ), "Provided max threshold must be a number"
   except AssertionError as e:
     raise InvalidExpectationConfigurationError(str(e))
