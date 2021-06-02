import great_expectations as ge

# add great_expectations/plugins to path
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'great_expectations'))

from plugins import column_custom_max_expectation

context = ge.get_context()
context.run_checkpoint(checkpoint_name="my_checkpoint_with_custom_expectation")
context.open_data_docs()
