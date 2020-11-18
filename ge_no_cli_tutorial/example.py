import os
import logging

from great_expectations.data_context import BaseDataContext 
from great_expectations.data_context.types.base import DataContextConfig

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)



def print_bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    print('\n'.join(res))


# https://docs.greatexpectations.io/en/latest/guides/workflows_patterns/deployment_hosted_environments.html#step-1-configure-your-data-context
def configure_data_context():
    def abs_path(relative_path):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_path)

    print_bordered("Step 1: Configure your Data Context")
    project_config = DataContextConfig(
        config_version=2,
        plugins_directory=None,
        config_variables_file_path=None,
        datasources={
            "my_postgres_db": {
                "data_asset_type": {
                    "class_name": "SqlAlchemyDataset",
                    "module_name": "great_expectations.dataset",
                },
                "class_name": "SqlAlchemyDatasource",
                "module_name": "great_expectations.datasource",
                "batch_kwargs_generators": {},
                "credentials": {
                    "drivername": "postgresql",
                    "host": "localhost",
                    "port": "65432",
                    "username": "ge_tutorials",
                    "password": "ge_tutorials",
                    "database": "ge_tutorials"
                }
            },
        },
        stores={
            "expectations_store": {
                "class_name": "ExpectationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": abs_path("expectations/")
                }
            },
            "validations_store": {
                "class_name": "ValidationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": abs_path("uncommitted/validations/")
                },
            },
            "evaluation_parameter_store": {
                "class_name": "EvaluationParameterStore"
            }
        },
        expectations_store_name="expectations_store",
        validations_store_name="validations_store",
        evaluation_parameter_store_name="evaluation_parameter_store",
        data_docs_sites={
            "local_site": {
                "class_name": "SiteBuilder",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": abs_path("uncommitted/data_docs/local_site/")
                },
                "site_index_builder": {
                    "class_name": "DefaultSiteIndexBuilder",
                },
                "show_how_to_buttons": True,
            }
        },
        validation_operators={
            "action_list_operator": {
                "class_name": "ActionListValidationOperator",
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {"class_name": "StoreValidationResultAction"},
                    },
                    {
                        "name": "store_evaluation_params",
                        "action": {"class_name": "StoreEvaluationParametersAction"},
                    },
                    {
                        "name": "update_data_docs",
                        "action": {"class_name": "UpdateDataDocsAction"},
                    },
                ],
            }
        },
        anonymous_usage_statistics={
          "enabled": True
        }
    )
    return BaseDataContext(project_config=project_config)


# https://docs.greatexpectations.io/en/latest/guides/workflows_patterns/deployment_hosted_environments.html#step-2-create-expectation-suites-and-add-expectations
def create_expectations(context):
    print_bordered("Step 2.1: Create Expectation Suite")
    suite = context.create_expectation_suite(
        "my_suite_name", overwrite_existing=True
    )
    batch_kwargs = {
        "datasource": "my_postgres_db",
        "schema": "public",
        "table": "yellow_tripdata_sample_2019_01",
    }
    batch = context.get_batch(batch_kwargs, suite)

    print_bordered("Step 2.2: Add Expectations")
    batch.expect_column_values_to_not_be_null("fare_amount")
    batch.save_expectation_suite(discard_failed_expectations=False)
    return batch


# https://docs.greatexpectations.io/en/latest/guides/workflows_patterns/deployment_hosted_environments.html#step-3-run-validation
def run_validation(batch):
    print_bordered("Step 3: Run validation")

    results = context.run_validation_operator(
        "action_list_operator",
        assets_to_validate=[batch],
        run_id="my_run_id")


context = configure_data_context()
batch = create_expectations(context)
run_validation(batch)
