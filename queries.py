import mysql.connector
from connection_config import Connection

cn = Connection()

connect = mysql.connector.connect(user='root', host = '127.0.0.1', port = '3306', passwd = cn.password, db = cn.database , buffered = True)
connect.autocommit = True

def query_cocktail(cocktail):
    cur = connect.cursor()
    query = f"select * from cocktails where cocktail_name = %s"
    cur.execute(query, (cocktail,))
    result = cur.fetchone()

    if result:
        instructions_query = f"select instructions from cocktail_instructions where cocktail_id = %s"
        cur.execute(instructions_query, (result[0],))
        instructions = cur.fetchone()[0]

        ### Query the cocktail_ingredients table joined with the ingredients table 
        ### on matching ingredient id where the cocktail_id corresponds to
        #  the desired cocktail
        ingredient_measures_query = f"""select c.ingredient_measure, i.ingredient_name from
                    ingredients i join cocktail_ingredients c on 
                    i.id = c.ingredient_id where c.cocktail_id = %s"""
        cur.execute(ingredient_measures_query, (result[0],))
        ingredient_measures = cur.fetchall()

        ingredient_measures_list = []
        for item in ingredient_measures:
            append_items = item[0] + " " + item[1]
            ingredient_measures_list.append(append_items)

        details = {"name" : result[1], "category" : result[2], 
        "IBA_category": result[3], "alcoholic" : result[4],
        "glass": result[6], "instructions" : instructions,
        "ingredient measures" : ingredient_measures_list}
        return details
    else:
        return {}

def query_ingredient(ingredient):
    cur = connect.cursor()
    query = f"select * from ingredients where ingredient_name = %s"
    cur.execute(query, (ingredient,))
    result = cur.fetchone()
    
    if result:
        if result[2]:
            return (result[0], result[2])
        else:
            print("\nIngredient currently has no description listed.")
            return [result[0]]
    else:
        print("\nIngredient not found.")
        return [-10]



def insert_drink_details(drink_details):
    if not query_cocktail(drink_details["name"]):
        cur = connect.cursor()
        query_drink_detail_insert = f"""insert into cocktails (cocktail_name, category, IBA_category,
                                    alcoholic, foreign_id, glass) values (%s, %s, %s, %s, %s, %s)"""
        cur.execute(query_drink_detail_insert, (drink_details["name"], 
                    drink_details["category"], drink_details["IBA_category"], 
                    drink_details["alcoholic"], drink_details["foreign_id"], 
                    drink_details["glass"]))
        
        query_new_drink_id = f"""select id from cocktails where cocktail_name = %s"""
        cur.execute(query_new_drink_id, (drink_details["name"],))
        drink_id = cur.fetchone()[0]

        query_instructions_insert = f"""insert into cocktail_instructions 
                                        (cocktail_id, instructions) values (%s, %s)"""

        cur.execute(query_instructions_insert, (drink_id, drink_details["instructions"]))

        query_ingredient_ids = f"select id from ingredients where ingredient_name = %s"

        ingredients_list = []
        for ingredient in drink_details["ingredient measures"]:
            new_item = ingredient[1]
            ingredients_list.append(new_item)

        ingredient_ids_list = []
        for item in ingredients_list:
            cur.execute(query_ingredient_ids, (item,))
            result = cur.fetchone()
            if result:
                ingredient_ids_list.append(result[0])
            else:
                insert_ingredient_query = f"insert into ingredients (ingredient_name) values (%s)"
                cur.execute(insert_ingredient_query, (item,))
                new_ingredient_query = f"select id from ingredients where ingredient_name = %s"
                cur.execute(new_ingredient_query, (item,))
                new_id_result = cur.fetchone()[0]
                ingredient_ids_list.append(new_id_result)
        
        insert_cocktail_ingredients_query = f"""insert into cocktail_ingredients 
                                                (cocktail_id, ingredient_id, ingredient_measure)
                                                values (%s, %s, %s)"""

        measures_list = []
        for measure in drink_details["ingredient measures"]:
            new_item = measure[0]
            measures_list.append(new_item)

        for item in zip(ingredient_ids_list, measures_list):
            cur.execute(insert_cocktail_ingredients_query, (drink_id, item[0], item[1]))


def insert_ingredient_description(ingredient_name, description):
    cur = connect.cursor()
    insert_ingredient_desc_query = f"""update ingredients set description = %s where ingredient_name = %s
     and description is null"""
    cur.execute(insert_ingredient_desc_query, (description, ingredient_name))