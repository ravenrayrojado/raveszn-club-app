from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/terms", response_class=HTMLResponse)
def terms():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAVESZN CLUB! — Terms of Service</title>
    <style>
        body {
            margin: 0;
            padding: 40px 20px;
            background: #111214;
            color: #f2f3f5;
            font-family: Arial, sans-serif;
            line-height: 1.7;
        }

        main {
            max-width: 800px;
            margin: auto;
            background: #1e1f22;
            padding: 40px;
            border-radius: 20px;
        }

        h1 {
            margin-top: 0;
        }

        h2 {
            margin-top: 32px;
        }

        .updated {
            color: #b5bac1;
        }
    </style>
</head>

<body>
<main>

<h1>RAVESZN CLUB! — Terms of Service</h1>

<p class="updated">Last updated: September 3, 2026</p>

<p>
Welcome to RAVESZN CLUB!. These Terms of Service explain the rules
for using the RAVESZN CLUB! Discord application.
</p>

<h2>1. Acceptance of Terms</h2>

<p>
By installing or using the RAVESZN CLUB! application, you agree to
these Terms of Service. If you do not agree, please do not use the
application.
</p>

<h2>2. Use of the Application</h2>

<p>
RAVESZN CLUB! provides features and functionality for the
RAVESZN CLUB! Discord community. You agree to use the application
lawfully and in accordance with Discord's rules and policies.
</p>

<h2>3. Discord</h2>

<p>
RAVESZN CLUB! operates through Discord. Your use of Discord remains
subject to Discord's Terms of Service, Community Guidelines, and
other applicable policies.
</p>

<h2>4. Availability</h2>

<p>
We may modify, update, suspend, or discontinue the application or
any of its features at any time.
</p>

<h2>5. Prohibited Use</h2>

<p>
You may not use the application to abuse, harass, spam, exploit,
disrupt, or otherwise misuse Discord or other users.
</p>

<h2>6. Disclaimer</h2>

<p>
The application is provided on an "as is" and "as available" basis.
We do not guarantee that the application will always be available
or error-free.
</p>

<h2>7. Changes</h2>

<p>
These Terms may be updated from time to time. Continued use of the
application after changes are published means you accept the
updated Terms.
</p>

<h2>8. Contact</h2>

<p>
For questions about these Terms, please contact the RAVESZN CLUB!
server administration team through the official Discord server.
</p>

</main>
</body>
</html>
"""


@app.get("/privacy", response_class=HTMLResponse)
def privacy():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAVESZN CLUB! — Privacy Policy</title>
    <style>
        body {
            margin: 0;
            padding: 40px 20px;
            background: #111214;
            color: #f2f3f5;
            font-family: Arial, sans-serif;
            line-height: 1.7;
        }

        main {
            max-width: 800px;
            margin: auto;
            background: #1e1f22;
            padding: 40px;
            border-radius: 20px;
        }

        h1 {
            margin-top: 0;
        }

        h2 {
            margin-top: 32px;
        }

        .updated {
            color: #b5bac1;
        }
    </style>
</head>

<body>
<main>

<h1>RAVESZN CLUB! — Privacy Policy</h1>

<p class="updated">Last updated: September 3, 2026</p>

<p>
This Privacy Policy explains how the RAVESZN CLUB! Discord
application handles information when you use it.
</p>

<h2>1. Information We Collect</h2>

<p>
RAVESZN CLUB! only accesses information necessary for the features
provided by the application and permitted through Discord's
authorization system.
</p>

<h2>2. How Information Is Used</h2>

<p>
Information accessed by the application is used to provide,
maintain, and improve the application's functionality within
Discord.
</p>

<h2>3. Information Sharing</h2>

<p>
We do not sell your personal information. We do not intentionally
share personal information with third parties except where
necessary to operate the application or comply with applicable law.
</p>

<h2>4. Data Retention</h2>

<p>
Information is retained only for as long as reasonably necessary
to provide the application's functionality, maintain security,
or meet legal requirements.
</p>

<h2>5. Discord</h2>

<p>
Because the application operates through Discord, Discord may
independently collect and process information according to
Discord's own Privacy Policy.
</p>

<h2>6. Security</h2>

<p>
Reasonable measures are used to protect information handled by
the application. However, no online service can guarantee
absolute security.
</p>

<h2>7. Changes to This Policy</h2>

<p>
This Privacy Policy may be updated when the application's
functionality or data practices change.
</p>

<h2>8. Contact</h2>

<p>
For questions about this Privacy Policy, please contact the
RAVESZN CLUB! server administration team through the official
Discord server.
</p>

</main>
</body>
</html>
"""


@app.get("/")
def home():
    return {
        "name": "RAVESZN CLUB!",
        "status": "online"
    }
