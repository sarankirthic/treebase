# app.py
from flask import Flask, request, jsonify, redirect
from sqlalchemy.exc import IntegrityError
from db import SessionLocal, engine
from models import Base, URL
from hashids import Hashids
from Config import config

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
hashids = Hashids(min_length=6, salt=config.SECRET)


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify({"error": "Missing URL"}), 400

    if not original_url.startswith(("http://", "https://")):
        original_url = "http://" + original_url

    session = SessionLocal()
    try:
        new_url = URL(original_url=original_url)
        session.add(new_url)
        session.commit()

        short_hash = hashids.encode(new_url.id)
        new_url.short_url = short_hash
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Could not shorten URL"}), 500
    finally:
        session.close()

    return jsonify({"short_url": request.host_url + short_hash})


@app.route("/<short_url>")
def redirect_url(short_url):
    session = SessionLocal()
    try:
        decoded = hashids.decode(short_url)
        print(decoded)
        if not decoded:
            print(short_url)
            return jsonify({"error": "Invalid URL"}), 404

        url_id = decoded[0]
        url = session.query(URL).filter(URL.id == url_id).first()
        if url:
            return redirect(url.original_url, code=301)
        else:
            return jsonify({"error": "URL not found"}), 404
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)
