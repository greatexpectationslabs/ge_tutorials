from great_expectations.execution_engine import (
   PandasExecutionEngine,
   SparkDFExecutionEngine,
   SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.metrics import (
   ColumnMetricProvider,
   column_aggregate_value, column_aggregate_partial,
)
from great_expectations.expectations.metrics.import_manager import F, sa

class ColumnCustomMax(ColumnMetricProvider):
    """MetricProvider Class for Custom Aggregate Max MetricProvider"""

    metric_name = "column.aggregate.custom.max"

    @column_aggregate_value(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        """Pandas Max Implementation"""
        return column.max()

    @column_aggregate_partial(engine=SqlAlchemyExecutionEngine)
    def _sqlalchemy(cls, column, **kwargs):
        """SqlAlchemy Max Implementation"""
        return sa.func.max(column)

    @column_aggregate_partial(engine=SparkDFExecutionEngine)
    def _spark(cls, column, _table, _column_name, **kwargs):
        """Spark Max Implementation"""
        types = dict(_table.dtypes)
        return F.maxcolumn()
