from great_expectations.core import ExpectationConfiguration
from great_expectations.execution_engine import ExecutionEngine 
from great_expectations.expectations.expectation import ColumnExpectation
from typing import Dict 


class ExpectColumnMaxToBeBetweenCustom(ColumnExpectation):
   # Setting necessary computation metric dependencies and defining kwargs, as well as assigning kwargs default values
   metric_dependencies = ("column.aggregate.custom.max",)
   success_keys = ("min_value", "strict_min", "max_value", "strict_max")

   # Default values
   default_kwarg_values = {
       "row_condition": None,
       "condition_parser": None,
       "min_value": None,
       "max_value": None,
       "strict_min": None,
       "strict_max": None,
       "mostly": 1
   }

   def _validate(
      self,
      configuration: ExpectationConfiguration,
      metrics: Dict,
      runtime_configuration: dict = None,
      execution_engine: ExecutionEngine = None,
   ):
      """Validates the given data against the set minimum and maximum value thresholds for the column max"""
      column_max = metrics.get("column.aggregate.max")

      # Obtaining components needed for validation
      min_value = self.get_success_kwargs(configuration).get("min_value")
      strict_min = self.get_success_kwargs(configuration).get("strict_min")
      max_value = self.get_success_kwargs(configuration).get("max_value")
      strict_max = self.get_success_kwargs(configuration).get("strict_max")

      # Checking if mean lies between thresholds
      if min_value is not None:
          if strict_min:
              above_min = column_max > min_value
          else:
              above_min = column_max >= min_value
      else:
          above_min = True

      if max_value is not None:
          if strict_max:
              below_max = column_max < max_value
          else:
              below_max = column_max <= max_value
      else:
          below_max = True

      success = above_min and below_max

      return {"success": success, "result": {"observed_value": column_max}}
