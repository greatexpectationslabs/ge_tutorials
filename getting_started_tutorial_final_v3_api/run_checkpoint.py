import great_expectations as ge

context = ge.get_context()
context.run_checkpoint(checkpoint_name="my_checkpoint_with_custom_expectation")
context.open_data_docs()
