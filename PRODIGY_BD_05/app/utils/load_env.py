import os

# Charger manuellement les variables du fichier .env
def load_env_file(filepath=".env"):
    try:
        with open(filepath) as f:
            for line in f:
                if line.strip() == "" or line.startswith("#"):
                    continue
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    except FileNotFoundError:
        print(f"Fichier {filepath} non trouvé.")
