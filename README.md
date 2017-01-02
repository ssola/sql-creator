# sql-creator

This small script creates a HIVE database given some parameters.

Ex.

```
python sql-creator.py --database database_name --table table_name --fields "country|s inserted_at|i value|bi is_vip_customer|b" --partition-by "day|i" --base-path "/my_company/databases" --output-path "/my_company/queries/"
```

Generates this SQL output:

```sql
CREATE EXTERNAL TABLE database_name.table_name (
    country STRING,
    is_vip_customer BOOLEAN,
    value BIGINT,
    inserted_at INT
    ) PARTITIONED BY (day INT)
STORED AS PARQUET
LOCATION '/my_company/databases/database_name/table_name';
DONE! check here /my_company/queries/database_name/table_name.sql
```
