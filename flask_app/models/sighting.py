from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Sighting:
    db_name = 'belt_exam'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.what_happened = db_data['what_happened']
        self.date_of = db_data['date_of']
        self.num_of = db_data['num_of']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location, what_happened, date_of, num_of,user_id) VALUES (%(location)s, %(what_happened)s, %(date_of)s, %(num_of)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_sightings = []
        for row in results:
            print(row['date_of'])
            all_sightings.append( cls(row) )
        return all_sightings
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s,what_happened=%(what_happened)s,date_of=%(date_of)s, num_of=%(num_of)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM sightings WHERE id =%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_sighting(sighting): 
        is_valid = True
        if len(sighting['location']) < 3:
            is_valid = False
            flash("Area must be at least 3 characters long!")
        if len(sighting['what_happened']) < 3:
            is_valid = False
            flash("Give us some better details!")
        if sighting['date_of'] == "":
            is_valid = False
            flash("Please select the date the sighting happened")
        return is_valid