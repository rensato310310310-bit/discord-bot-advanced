import requests
from flask import Blueprint, redirect, render_template, request, session

from bot.config import config
from bot.utils.db import save_auth_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login_page():
    return render_template("login.html")


@auth_bp.route("/discord-login")
def discord_login():
    oauth_url = (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={config.DISCORD_CLIENT_ID}"
        "&redirect_uri=http://localhost:5000/auth/callback"
        "&response_type=code"
        "&scope=identify+email"
    )
    return redirect(oauth_url)


@auth_bp.route("/auth/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "認証コードがありません。", 400

    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": config.DISCORD_CLIENT_ID,
            "client_secret": config.DISCORD_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.DISCORD_REDIRECT_URI,
            "scope": "identify email",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token_data = token_response.json()

    if "access_token" not in token_data:
        return "Discord 認証に失敗しました。", 400

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token")
    expires_at = token_data.get("expires_in")

    user_response = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_data = user_response.json()

    session["discord_user_id"] = user_data.get("id")
    session["discord_email"] = user_data.get("email")

    save_auth_user(
        discord_user_id=user_data.get("id"),
        email=user_data.get("email"),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )

    return render_template("auth_success.html")
