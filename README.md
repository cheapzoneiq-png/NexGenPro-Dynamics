{
  "version": 2,
  "builds": ,  <!-- Missing information -->
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
if __name__ == '__main__':
    app.run()  # For local
application = app  # Vercel needs this{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
flask
stripe
requests
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
{
  "version": 2,
  "builds": ,
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}flask
stripe
requests
gunicorn
if __name__ == '__main__':
app.run()
application = app # Vercel hook

