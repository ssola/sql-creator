import os
from argparse import ArgumentParser

import errno
from jinja2 import Environment, FileSystemLoader


def parse_input_arguments():
    arg_parser = ArgumentParser()

    arg_parser.add_argument('--database', dest='database',
                            required=True)
    arg_parser.add_argument('--table', dest='table', required=True)

    arg_parser.add_argument('--fields', dest='fields', required=True)

    arg_parser.add_argument('--partition-by', dest='partition_by',
                            required=False)
    arg_parser.add_argument('--base-path', dest='base_path', required=True)

    arg_parser.add_argument('--output-path', dest='output_path', required=True)

    return arg_parser.parse_args()


def parse_fields(fields):
    final_fields = {}
    mapper = {
        "s":  "STRING",
        "i": "INT",
        "f": "FLOAT",
        "d": "DOUBLE",
        "bi": "BIGINT",
        "b": "BOOLEAN"
    }

    fields = fields.split(" ")

    for field in fields:
        field_parts = field.split("|")
        final_fields[field_parts[0]] = mapper[field_parts[1]]

    return final_fields


def generate_output(
        database, table, fields, partition_by, base_path
):
    fields = parse_fields(fields)
    partition_by = parse_fields(partition_by)

    jinja = Environment(
        loader=FileSystemLoader(
            searchpath=os.path.dirname(os.path.realpath(__file__))
        )
    )

    template = jinja.get_template("hive_sql_template.jinja")

    output = template.render(
        {
            "database": database,
            "table": table,
            "fields": fields,
            "partition_by": partition_by,
            "base_path": base_path
        }
    )

    return output


def save_file(file_path, output):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(file_path, "w") as f:
        f.write(output)


if __name__ == '__main__':
    args = parse_input_arguments()

    if not os.path.exists(args.output_path):
        raise ValueError("Output {} does not exists".format(args.output_path))

    output = generate_output(
        args.database, args.table, args.fields, args.partition_by,
        args.base_path
    )

    final_file_path = os.path.join(
        args.output_path,
        args.database,
        "{}.sql".format(args.table)
    )

    save_file(final_file_path, output)

    print output
    print "DONE! check here {}".format(final_file_path)
