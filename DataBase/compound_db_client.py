import mysql.connector

COMPOUND = "compound"
HEALTH_EFFECTS = "health_effects"

compound_table_name = "Compound"
compound_name_col_name = "name"
compound_id_col_name = "id"

compound_health_effect_table_name = "CompoundsHealthEffect"
compound_health_effect_compound_id_col_name = "compound_id"
compound_health_effect_he_id_col_name = "health_effect_id"

health_effect_table_name = "HealthEffect"
health_effect_id_col_name = "id"


def get_strings_formatter(strings_len):
    return ','.join(['%s'] * strings_len)


class CompoundDBClient:

    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(user=user, password=password, host=host, database=database)

    def open_cursor(self):
        return self.connection.cursor(dictionary=True)
    
    def close_connection(self):
        if self.connection:
            self.connection.close()

    def fetch_compound_by_name(self, compound_name):
        compound_name = [compound.upper() for compound in compound_name]
        cursor = self.open_cursor()
        query_string = f"SELECT * FROM {compound_table_name} " \
                       f"WHERE UPPER({compound_name_col_name}) = %s"
        cursor.execute(query_string, compound_name)
        row = cursor.fetchone()
        cursor.close()
        return row

    def fetch_compound_health_effect(self, compound_id):
        cursor = self.open_cursor()
        query_string = f"SELECT * FROM {compound_health_effect_table_name} WHERE " \
                       f"{compound_health_effect_compound_id_col_name} = %s"
        cursor.execute(query_string, compound_id)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_health_effect(self, health_effect_id):
        cursor = self.open_cursor()
        query_string = f"SELECT * FROM {health_effect_table_name} " \
                       f"WHERE {health_effect_id_col_name} = %s"
        cursor.execute(query_string, health_effect_id)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_expanded_compound(self, compound_name):
        # compound_name = [compound.upper() for compound in compound_name]
        cursor = self.open_cursor()
        compound = self.fetch_compound_by_name(compound_name)
        if not compound:
            print(f"No compound having name {compound_name} found")
            return None

        compound_health_effect_mappings = self.fetch_compound_health_effect([compound[compound_id_col_name]])
        compound_health_effects = []
        for compound_health_effect_mapping in compound_health_effect_mappings:
            health_effect = \
                self.fetch_health_effect([compound_health_effect_mapping[compound_health_effect_he_id_col_name]])
            compound_health_effects.append(health_effect)

        expanded_compound = {
            COMPOUND: compound,
            HEALTH_EFFECTS: compound_health_effects
        }
        cursor.close()
        return expanded_compound

    def fetch_compounds_by_names(self, names: list[str]):
        cursor = self.connection.cursor(dictionary=True)
        format_names = get_strings_formatter(len(names))
        query_string = f"SELECT * " \
                       f"FROM {compound_table_name} " \
                       f"WHERE {compound_name_col_name} IN (%s)" % format_names
        cursor.execute(query_string, tuple(names))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_health_effects_by_ids(self, ids: list[str]):
        cursor = self.connection.cursor(dictionary=True)
        format_names = get_strings_formatter(len(ids))
        query_string = f"SELECT * " \
                       f"FROM {health_effect_table_name} " \
                       f"WHERE {health_effect_id_col_name} IN (%s)" % format_names
        cursor.execute(query_string, tuple(ids))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_compound_health_effect_mappings(self, compound_ids: list[str]):
        cursor = self.connection.cursor(dictionary=True)
        format_ids = get_strings_formatter(len(compound_ids))
        query_string = f"SELECT " \
                       f"{compound_health_effect_compound_id_col_name}, " \
                       f"{compound_health_effect_he_id_col_name} " \
                       f"FROM {compound_health_effect_table_name} " \
                       f"WHERE {compound_health_effect_compound_id_col_name} IN (%s)" % format_ids
        cursor.execute(query_string, tuple(compound_ids))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_expanded_compounds(self, compound_names: list[str]):
        # fetch compounds by name and map them to their id
        compounds = self.fetch_compounds_by_names(compound_names)
        compound_by_id = {}
        for compound in compounds:
            compound_id = compound[compound_id_col_name]
            compound_by_id[compound_id] = compound
        compound_ids = list(compound_by_id.keys())

        # fetch compounds - health effects mapping
        compound_health_effect_mappings = self.fetch_compound_health_effect_mappings(compound_ids)

        # fetch health effects by ids and map them to their id
        health_effect_ids = []
        for mapping in compound_health_effect_mappings:
            health_effect_ids.append(mapping[compound_health_effect_he_id_col_name])

        health_effects = self.fetch_health_effects_by_ids(health_effect_ids)
        health_effect_by_id = {}
        for health_effect in health_effects:
            health_effect_id = health_effect[health_effect_id_col_name]
            health_effect_by_id[health_effect_id] = health_effect

        # create expanded compounds
        expanded_compounds = {}
        for compound_id in compound_ids:
            compound_expanded_health_effects = {}
            for mapping in compound_health_effect_mappings:
                compound_id_m = mapping[compound_health_effect_compound_id_col_name]
                if compound_id_m == compound_id:
                    health_effect_id_m = mapping[compound_health_effect_he_id_col_name]
                    compound_expanded_health_effects[health_effect_id_m] = \
                        health_effect_by_id[health_effect_id_m]
            expanded_compounds[compound_id] = \
                {"compound": compound_by_id[compound_id], "health_effects": compound_expanded_health_effects}

        return expanded_compounds


    # def fetch_compound_test(self):
    #     cursor = self.open_cursor()
    #     query_string = f"SELECT * FROM {compound_table_name} LIMIT 10"
    #     cursor.execute(query_string)
    #     row = cursor.fetchall()
    #     cursor.close()
    #     return row

