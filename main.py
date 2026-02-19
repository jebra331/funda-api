from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

# توکن مخفی (حتماً این رو به یک مقدار امن تغییر بده)
SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "my-secret-token-123")

# داده‌های اولیه فاندا
funda_data = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    "funda_score": 0.0,
    "sentiment": "neutral",
    "confidence": 50,
    "summary": "Waiting for first analysis...",
    "price_now": 0.0
}

@app.route('/')
def root():
    return jsonify({
        "message": "Funda Score API is running!",
        "status": "active",
        "endpoints": ["/api/funda", "/api/update", "/api/health"]
    })

@app.route('/api/funda', methods=['GET'])
def get_funda():
    """دریافت آخرین امتیاز فاندا"""
    funda_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    return jsonify(funda_data)

@app.route('/api/update', methods=['POST'])
def update_funda():
    """بروزرسانی امتیاز فاندا (فقط برای دستیار هوش مصنوعی)"""
    auth = request.headers.get('Authorization')
    if auth != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # بروزرسانی فیلدهایی که در درخواست آمده‌اند
    for key in ['funda_score', 'sentiment', 'confidence', 'summary', 'price_now']:
        if key in data:
            funda_data[key] = data[key]

    funda_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    return jsonify({"status": "ok", "updated": funda_data["timestamp"]})

@app.route('/api/health', methods=['GET'])
def health():
    """بررسی سلامت سرویس"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })
@app.route('/api/test-update', methods=['GET'])
def test_update():
    """نقطه تست برای آپدیت دستی (بدون نیاز به توکن)"""
    global funda_data
    funda_data.update({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "funda_score": 3.2,
        "sentiment": "bullish",
        "confidence": 85,
        "summary": "Test update from browser",
        "price_now": 4972
    })
    return jsonify({"status": "ok", "data": funda_data})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)