import pandas as pd
import pytest

from great_expectations.core.expectation_validation_result import (
    ExpectationValidationResult,
)
from great_expectations.self_check.util import (
    build_pandas_validator_with_data,
    build_sa_validator_with_data,
)
from great_expectations.util import is_library_loadable


@pytest.mark.skipif(
    not is_library_loadable(library_name="pyathena"),
    reason="pyathena is not installed",
)
def test_expect_column_values_to_be_in_type_list_dialect_pyathena(sa):
    from pyathena import sqlalchemy_athena

    df = pd.DataFrame({"col": ["test_val1", "test_val2"]})
    validator = build_sa_validator_with_data(df, "sqlite")

    # Monkey-patch dialect for testing purposes.
    validator.execution_engine.dialect_module = sqlalchemy_athena

    result = validator.expect_column_values_to_be_in_type_list(
        "col", type_list=["STRINGTYPE", "BOOLEAN"]
    )
    assert result == ExpectationValidationResult(
        success=True,
        expectation_config={
            "expectation_type": "expect_column_values_to_be_in_type_list",
            "kwargs": {
                "column": "col",
                "type_list": ["STRINGTYPE", "BOOLEAN"],
            },
            "meta": {},
        },
        result={
            "element_count": 2,
            "unexpected_count": 0,
            "unexpected_percent": 0.0,
            "partial_unexpected_list": [],
            "missing_count": 0,
            "missing_percent": 0.0,
            "unexpected_percent_total": 0.0,
            "unexpected_percent_nonmissing": 0.0,
        },
        exception_info={
            "raised_exception": False,
            "exception_traceback": None,
            "exception_message": None,
        },
        meta={},
    )


def test_expect_column_values_to_be_in_type_list_nullable_int():
    from packaging.version import parse

    pandas_version = parse(pd.__version__)
    if pandas_version < parse("0.24"):
        # Prior to 0.24, Pandas did not have
        pytest.skip("Prior to 0.24, Pandas did not have `Int32Dtype` or related.")

    df = pd.DataFrame({"col": pd.Series([1, 2, None], dtype=pd.Int32Dtype())})
    validator = build_pandas_validator_with_data(df)

    result = validator.expect_column_values_to_be_in_type_list(
        "col", type_list=["Int32Dtype"]
    )
    assert result == ExpectationValidationResult(
        success=True,
        expectation_config={
            "expectation_type": "expect_column_values_to_be_in_type_list",
            "kwargs": {
                "column": "col",
                "type_list": ["Int32Dtype"],
            },
            "meta": {},
        },
        result={
            "element_count": 3,
            "unexpected_count": 0,
            "unexpected_percent": 0.0,
            "partial_unexpected_list": [],
            "missing_count": 0,
            "missing_percent": 0.0,
            "unexpected_percent_total": 0.0,
            "unexpected_percent_nonmissing": 0.0,
        },
        exception_info={
            "raised_exception": False,
            "exception_traceback": None,
            "exception_message": None,
        },
        meta={},
    )
