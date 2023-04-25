import pandas as pd
from tqdm.notebook import tqdm


def parse_tables():
    
    tables_json = pd.read_json("gs://data_tql/spider/tables.json")
    row_table = []

    for i in tqdm(tables_json.iterrows(), total = len(tables_json)):

        schema_id = i[1]['db_id']
        row = i[1]
        for table_id in range(len(row['table_names'])):

            row_list = [schema_id]
            table_name = row['table_names'][table_id]
            row_list.append(table_name)
            table_name_original = row['table_names_original'][table_id]
            row_list.append(table_name_original)

            try:
                primary_key_index = row['primary_keys'][table_id]
                primary_key = row['column_names_original'][primary_key_index][-1]
                row_list.append(primary_key)
            except IndexError:
                row_list.append('NO_PRIMARY_KEY')

            temp_cols = []
            temp_cols_original = []
            temp_cols_dtypes = []

            for j in range(len(row['column_names'])):
                if (row['column_names'][j][0] == table_id):
                    temp_cols.append(row['column_names'][j][-1])
                    temp_cols_original.append(
                        row['column_names_original'][j][-1])
                    temp_cols_dtypes.append(row['column_types'][j])

            row_list.append(temp_cols)
            row_list.append(temp_cols_original)
            row_list.append(temp_cols_dtypes)

            foreign_keys = []
            for j in range(len(row['foreign_keys'])):
                left_index = row['foreign_keys'][j][0]
                right_index = row['foreign_keys'][j][1]

                left_table_name = row['table_names'][row['column_names_original'][left_index][0]]
                left_table_key = row['column_names_original'][left_index][1]
                right_table_name = row['table_names'][row['column_names_original'][right_index][0]]
                right_table_key = row['column_names_original'][right_index][1]

                if (primary_key == left_table_key or primary_key == right_table_key):
                    foreign_keys.append([left_table_name, left_table_key, right_table_name, right_table_key])

            row_list.append(foreign_keys)
            row_table.append(row_list)

    return pd.DataFrame(row_table, columns=[
        'schema_id',
        'table_name',
        'table_name_original',
        'primary_key',
        'column_list',
        'column_list_original',
        'column_datatypes',
        'foreign_keys'
    ])
