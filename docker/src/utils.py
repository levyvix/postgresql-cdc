from collections import defaultdict

from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

schemas = {
    "ORDERS": StructType(
        [
            StructField(
                "value",
                StructType(
                    [
                        StructField("before", StringType(), True),
                        StructField(
                            "after",
                            StructType(
                                [
                                    StructField("id", IntegerType(), True),
                                    StructField("user_id", IntegerType(), True),
                                    StructField("product_id", IntegerType(), True),
                                    StructField("quantity", IntegerType(), True),
                                    StructField("created_at", LongType(), True),
                                    StructField("updated_at", LongType(), True),
                                    StructField("deleted_at", StringType(), True),
                                ]
                            ),
                            True,
                        ),
                        StructField(
                            "source",
                            StructType(
                                [
                                    StructField("version", StringType(), True),
                                    StructField("connector", StringType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("ts_ms", LongType(), True),
                                    StructField("snapshot", StringType(), True),
                                    StructField("db", StringType(), True),
                                    StructField("sequence", StringType(), True),
                                    StructField("schema", StringType(), True),
                                    StructField("table", StringType(), True),
                                    StructField("txId", IntegerType(), True),
                                    StructField("lsn", LongType(), True),
                                    StructField("xmin", StringType(), True),
                                ]
                            ),
                            True,
                        ),
                        StructField("op", StringType(), True),
                        StructField("ts_ms", LongType(), True),
                        StructField("transaction", StringType(), True),
                    ]
                ),
                True,
            ),
        ]
    ),
    "PRODUCTS": StructType(
        [
            StructField(
                "value",
                StructType(
                    [
                        StructField("before", StringType(), True),
                        StructField(
                            "after",
                            StructType(
                                [
                                    StructField("id", IntegerType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("price", DoubleType(), True),
                                    StructField("created_at", LongType(), True),
                                    StructField("updated_at", LongType(), True),
                                    StructField("deleted_at", StringType(), True),
                                ]
                            ),
                            True,
                        ),
                        StructField(
                            "source",
                            StructType(
                                [
                                    StructField("version", StringType(), True),
                                    StructField("connector", StringType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("ts_ms", LongType(), True),
                                    StructField("snapshot", StringType(), True),
                                    StructField("db", StringType(), True),
                                    StructField("sequence", StringType(), True),
                                    StructField("schema", StringType(), True),
                                    StructField("table", StringType(), True),
                                    StructField("txId", IntegerType(), True),
                                    StructField("lsn", LongType(), True),
                                    StructField("xmin", StringType(), True),
                                ]
                            ),
                            True,
                        ),
                        StructField("op", StringType(), True),
                        StructField("ts_ms", LongType(), True),
                        StructField("transaction", StringType(), True),
                    ]
                ),
                True,
            ),
        ]
    ),
    "USERS": StructType(
        [
            StructField(
                "value",
                StructType(
                    [
                        StructField("before", StringType(), True),
                        StructField(
                            "after",
                            StructType(
                                [
                                    StructField("id", IntegerType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("email", StringType(), True),
                                    StructField("password", StringType(), True),
                                    StructField("created_at", LongType(), True),
                                    StructField("updated_at", LongType(), True),
                                    StructField("deleted_at", StringType(), True),
                                ]
                            ),
                            True,
                        ),
                        StructField(
                            "source",
                            StructType(
                                [
                                    StructField("version", StringType(), True),
                                    StructField("connector", StringType(), True),
                                    StructField("name", StringType(), True),
                                    StructField("ts_ms", LongType(), True),
                                    StructField("snapshot", StringType(), True),
                                    StructField("db", StringType(), True),
                                    StructField("sequence", StringType(), True),
                                    StructField("schema", StringType(), True),
                                    StructField("table", StringType(), True),
                                    StructField("txId", IntegerType(), True),
                                    StructField("lsn", LongType(), True),
                                    StructField("xmin", StringType(), True),
                                ]
                            ),
                            True,
                        ),
                        StructField("op", StringType(), True),
                        StructField("ts_ms", LongType(), True),
                        StructField("transaction", StringType(), True),
                    ]
                ),
                True,
            ),
        ]
    ),
}
