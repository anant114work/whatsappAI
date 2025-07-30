from app import app

def list_routes():
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} {rule.rule}")

if __name__ == "__main__":
    list_routes()