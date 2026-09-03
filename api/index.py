from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import os
import secrets
import requests

app = FastAPI()

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")

REDIRECT_URI = "https://raveszn-club-app.vercel.app/api/callback"

DISCORD_API = "https://discord.com/api/v10"


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/api")
def api_home():
    return {
        "status": "online",
        "message": "RAVESZN CLUB! App is working."
    }


@app.get("/api/connect")
def connect():
    state = secrets.token_urlsafe(32)

    discord_url = (
        "https://discord.com/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=identify%20role_connections.write"
        f"&state={state}"
    )

    response = RedirectResponse(discord_url)

    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=600
    )

    return response


@app.get("/api/callback")
def callback(request: Request, code: str = None, state: str = None):

    saved_state = request.cookies.get("oauth_state")

    if not code:
        return HTMLResponse(
            "<h2>Missing authorization code.</h2>",
            status_code=400
        )

    if not state or state != saved_state:
        return HTMLResponse(
            "<h2>Invalid OAuth state.</h2>",
            status_code=400
        )

    # Exchange authorization code for access token
    token_response = requests.post(
        f"{DISCORD_API}/oauth2/token",
        data={
            "client_id": DISCORD_CLIENT_ID,
            "client_secret": DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        timeout=15
    )

    if token_response.status_code != 200:
        return HTMLResponse(
            "<h2>Discord OAuth token exchange failed.</h2>"
            f"<pre>{token_response.text}</pre>",
            status_code=400
        )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return HTMLResponse(
            "<h2>No Discord access token received.</h2>",
            status_code=400
        )

    # Update the user's application role connection
    connection_response = requests.put(
        f"{DISCORD_API}/users/@me/applications/{DISCORD_CLIENT_ID}/role-connection",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={
            "platform_name": "RAVESZN CLUB!",
            "platform_username": "RAVESZN CLUB!",
            "metadata": {}
        },
        timeout=15
    )

    if connection_response.status_code not in (200, 204):
        return HTMLResponse(
            "<h2>Discord connection update failed.</h2>"
            f"<pre>{connection_response.text}</pre>",
            status_code=400
        )

    response = HTMLResponse("""
        <html>
        <head>
            <title>RAVESZN CLUB!</title>
        </head>
        <body style="
            background:#111;
            color:white;
            font-family:Arial,sans-serif;
            text-align:center;
            padding:80px 20px;
        ">
            <h1>RAVESZN CLUB! 🎉</h1>
            <p>Your Discord connection has been updated.</p>
            <p>You can close this window.</p>
        </body>
        </html>
    """)

    response.delete_cookie("oauth_state")

    return response
