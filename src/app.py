import config

connex_app = config.connex_app

# Create the application instance
connex_app.add_api('my_api.yaml')

if __name__ == '__main__':
    connex_app.run(debug=True)
