from server.app import ChiApp
from server.dev_settings import settings
import os

if __name__ == "__main__":
    env = os.environ.get("APP_ENV", "dev")
    print(f"Starting application in {env} mode")
    app = ChiApp('ChiApp', template_folder=settings['template_folder'])
    app.config.from_object(f"server.{env}_settings")
    app.config.update(
        dict(
            SECRET_KEY="powerful_secretkey",
            WTF_CSRF_SECRET_KEY="a csrf secret key"
        )
    )
    app.run(host='0.0.0.0', port=5000)