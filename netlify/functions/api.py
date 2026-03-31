from mangum import Mangum

from main import app


# Netlify Python Functions look for a top-level `handler`.
handler = Mangum(app)
