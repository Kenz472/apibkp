import requests
import re
import random
import string
from flask import Flask, request, jsonify

app = Flask(__name__)


# ==================== HELPER ====================
def generate_random_string(length=10):
    """Generate random string dengan huruf dan angka."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_video_url():
    """Ambil URL video dari viday.uk."""
    try:
        url_list = [
            "https://viday.uk/v/viral",
            "https://viday.uk/v/trending",
            "https://viday.uk/v/live",
            "https://viday.uk/v/populer"
        ]

        selected_url_base = random.choice(url_list)
        random_id = generate_random_string(10)
        api_url = f"{selected_url_base}={random_id}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }

        response = requests.get(api_url, headers=headers, timeout=30)
        html = response.text

        match = re.search(r'<source[^>]+src=["\']([^"\']+\.mp4)["\']', html, re.IGNORECASE)

        if not match:
            return {
                "status": False,
                "msg": "Video URL tidak ditemukan di halaman"
            }

        video_url = match.group(1)
        return {
            "status": True,
            "Url_Videos": video_url
        }

    except requests.exceptions.Timeout:
        return {"status": False, "msg": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"status": False, "msg": f"Request error: {str(e)}"}
    except Exception as e:
        return {"status": False, "msg": str(e)}


# ==================== ROUTES ====================
@app.route('/api/video', methods=['GET'])
def api_video():
    """Endpoint untuk mengambil URL video."""
    result = get_video_url()
    return jsonify(result)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": True, "msg": "OK"}), 200


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    """Handler untuk 404 Not Found."""
    return jsonify({
        "status": False,
        "error": "Not Found",
        "code": 404,
        "msg": f"Endpoint '{request.path}' tidak ditemukan"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handler untuk 405 Method Not Allowed."""
    return jsonify({
        "status": False,
        "error": "Method Not Allowed",
        "code": 405,
        "msg": f"Method '{request.method}' tidak diizinkan untuk '{request.path}'"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handler untuk 500 Internal Server Error."""
    return jsonify({
        "status": False,
        "error": "Internal Server Error",
        "code": 500,
        "msg": "Terjadi kesalahan pada server"
    }), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Handler untuk semua exception yang tidak tertangani."""
    return jsonify({
        "status": False,
        "error": "Internal Server Error",
        "code": 500,
        "msg": str(e)
    }), 500


# ==================== MAIN ====================
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)