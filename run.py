from app import app
from app.database.db_handler import DBHandler
from flask_jwt_extended import JWTManager

app.config['SECRET_KEY'] = 'maintenace_tracker_app_api777'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

if __name__ == '__main__':
    handler = DBHandler()
    handler.create_user_table()
    handler.create_requests_table()
    app.run(debug=True)
