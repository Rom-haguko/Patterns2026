import connexion

api = connexion.FlaskApp(__name__, specification_dir="./")
api.add_api("openapi.yaml")

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)
