
from flask_migrate import Migrate


from src.sqlalchemyModule.db_connection import app, db, api, docs


migrate = Migrate(app, db)

def create_resources():
    from src.routes.flask_routes import UsersApi, UsersApiGet, VerifyApi, LoginApi
    # define flask routes and link them to the api resource classes
    api.add_resource(UsersApi, '/users')
    api.add_resource(UsersApiGet, '/users/<string:user_id>')
    api.add_resource(VerifyApi, '/verify')
    api.add_resource(LoginApi, '/login')

    # register swagger docs to each api resource
    docs.register(UsersApi)
    docs.register(UsersApiGet)
    docs.register(VerifyApi)


def main():
    create_resources()
    app.run()


if __name__ == "__main__":
    main()
