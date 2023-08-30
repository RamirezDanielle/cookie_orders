from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


DB = "cookie_orders"
class Cookie:
    
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.cookie_type = data["cookie_type"]
        self.num_boxes = data["num_boxes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cookie_orders;"
        results = connectToMySQL(DB).query_db(query)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO cookie_orders
                ( name, cookie_type, num_boxes)
                VALUES
                (%(name)s, %(cookie_type)s, %(num_boxes)s);
                """
        return connectToMySQL(DB).query_db(query,data)
    
    @classmethod
    def get_one(cls, order_id):
        query = "SELECT * FROM cookie_orders WHERE id = %(id)s;"
        data = {"id":order_id}
        results = connectToMySQL(DB).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """ UPDATE cookie_orders SET
                    name = %(name)s, cookie_type = %(cookie_type)s, num_boxes = %(num_boxes)s
                    WHERE id = %(id)s;
                """
        results = connectToMySQL(DB).query_db(query,data)
        return results
    
    @staticmethod
    def validate_order(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Name must be at least 2 characters", )
            is_valid = False
        if len(data['cookie_type']) == 0:
            flash("Cookie type required" , 'update' )
            is_valid = False
        if len(data['num_boxes']) == 0:
            flash("Number of boxes required", 'update' )
            is_valid = False
        elif int(data['num_boxes']) <=0:
            flash("Number of boxes must be postive number", 'update')
            is_valid = False
        return is_valid