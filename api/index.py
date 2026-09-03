from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import os
import secrets
import requests

app = FastAPI()

# =========================================================
# SETTINGS
# =========================================================

DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

REDIRECT_URI = "https://raveszn-club-app.vercel.app/api/callback"

DISCORD_API = "https://discord.com/api/v10"


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return FileResponse("index.html")


# =========================================================
# API STATUS
# =========================================================

@app.get("/api")
def api_home():
    return {
        "status": "online",
        "message": "RAVESZN CLUB! App is working."
    }


# =========================================================
# TERMS OF SERVICE
# =========================================================

@app.get("/terms")
def terms():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAVESZN CLUB! - Terms of Service</title>
        <meta charset="UTF-8">
        <style>
            body {
                background: #111;
                color: white;
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 60px auto;
                padding: 20px;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <h1>RAVESZN CLUB! Terms of Service</h1>

        <p>
            By using the RAVESZN CLUB! Discord application,
            you agree to use the application responsibly and
            in accordance with Discord's Terms of Service.
        </p>

        <p>
            The application is provided as-is and may be
            modified, suspended, or discontinued at any time.
        </p>

        <p>
            RAVESZN CLUB! does not sell or share Discord
            account information for advertising purposes.
        </p>

        <p>
            By authorizing the application, you agree to
            these terms.
        </p>
    </body>
    </html>
    """)


# =========================================================
# PRIVACY POLICY
# =========================================================

@app.get("/privacy")
def privacy():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAVESZN CLUB! - Privacy Policy</title>
        <meta charset="UTF-8">
        <style>
            body {
                background: #111;
                color: white;
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 60px auto;
                padding: 20px;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <h1>RAVESZN CLUB! Privacy Policy</h1>

        <p>
            RAVESZN CLUB! uses Discord OAuth2 to authenticate
            users who choose to connect their Discord account.
        </p>

        <p>
            The application receives the information necessary
            to create and update the user's Discord application
            role connection.
        </p>

        <p>
            OAuth credentials are handled server-side and are
            not intentionally exposed publicly.
        </p>

        <p>
            RAVESZN CLUB! does not sell personal information.
        </p>
    </body>
    </html>
    """)


# =========================================================
# START DISCORD OAUTH
# =========================================================

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


# =========================================================
# LINKED ROLES VERIFICATION URL
#
# Discord can use this URL when the app is selected
# as a Linked Role verification method.
# =========================================================

@app.get("/api/verify-user")
def verify_user():
    return connect()


# =========================================================
# OAUTH CALLBACK
# =========================================================

@app.get("/api/callback")
def callback(
    request: Request,
    code: str = None,
    state: str = None
):

    # -----------------------------------------------------
    # Make sure Discord sent an authorization code
    # -----------------------------------------------------

    if not code:
        return HTMLResponse(
            "<h2>Missing Discord authorization code.</h2>",
            status_code=400
        )

    # -----------------------------------------------------
    # Verify OAuth state
    # -----------------------------------------------------

    saved_state = request.cookies.get("oauth_state")

    if not state or not saved_state or state != saved_state:
        return HTMLResponse(
            """
            <h2>Invalid OAuth state.</h2>
            <p>Please start the connection again.</p>
            """,
            status_code=400
        )

    # -----------------------------------------------------
    # Exchange Discord authorization code
    # for an OAuth access token
    # -----------------------------------------------------

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
            "<p>Please try again.</p>",
            status_code=400
        )

    token_data = token_response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        return HTMLResponse(
            "<h2>No Discord access token was received.</h2>",
            status_code=400
        )

    # -----------------------------------------------------
    # Update the user's Discord Role Connection
    # -----------------------------------------------------

    connection_response = requests.put(
        f"{DISCORD_API}/users/@me/applications/"
        f"{DISCORD_CLIENT_ID}/role-connection",

        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },

        json={
            "platform_name": "RAVESZN CLUB!",
            "platform_username": "RAVESZN CLUB!",
            "metadata": {
                "member": "1"
            }
        },

        timeout=15
    )

    if connection_response.status_code not in (200, 204):
        return HTMLResponse(
            "<h2>Discord connection update failed.</h2>"
            "<p>Please try connecting again.</p>",
            status_code=400
        )

    # -----------------------------------------------------
    # Success
    # -----------------------------------------------------

    response = HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RAVESZN CLUB!</title>

        <style>
            body {
                background: #111;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 80px 20px;
            }

            h1 {
                font-size: 32px;
            }

            p {
                font-size: 16px;
                color: #ccc;
            }
        </style>
    </head>

    <body>

        <h1>RAVESZN CLUB! 🎉</h1>

        <p>Your Discord connection has been updated.</p>

        <p>You can close this window.</p>

    </body>
    </html>
    """)

    response.delete_cookie("oauth_state")

    return response


# =========================================================
# REGISTER ROLE CONNECTION METADATA
# =========================================================

@app.get("/api/register-metadata")
def register_metadata():

    if not DISCORD_BOT_TOKEN:
        return {
            "status": "error",
            "message": "DISCORD_BOT_TOKEN is not configured."
        }

    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    metadata = [
        {
            "type": 7,
            "key": "member",
            "name": "SZN FAM",
            "description": "Member of RAVESZN CLUB!"
        }
    ]

    response = requests.put(
        f"{DISCORD_API}/applications/"
        f"{DISCORD_CLIENT_ID}/role-connections/metadata",

        headers=headers,
        json=metadata,
        timeout=15
    )

    try:
        discord_response = response.json()
    except Exception:
        discord_response = response.text

    return {
        "status_code": response.status_code,
        "discord_response": discord_response
    }
