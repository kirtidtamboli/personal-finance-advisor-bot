# Deployment

## Ngrok for Local Demo
To show the application publicly from your local machine:
1. Start the Flask server: `python run.py`
2. In a new terminal, start ngrok on port 5000: `ngrok http 5000`
3. Copy the `https://...ngrok.io` URL provided in the terminal.
4. Share the link!

*Note: Never commit your ngrok auth token.*

## Production Server
For production, use `gunicorn`:
```bash
gunicorn -w 4 'app:create_app("production")'
```
Set up Nginx as a reverse proxy.
Make sure to set `FLASK_ENV=production` and `DATABASE_URL` to your PostgreSQL instance.
