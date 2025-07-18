from app.main import app

# Vercel expects the app to be exported directly
# This is the ASGI application that Vercel will use
app = app
