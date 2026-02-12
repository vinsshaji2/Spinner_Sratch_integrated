from flask import Flask, render_template, jsonify, request, redirect, session
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.config["SECRET_KEY"] = "super_secret_key_123"  # Change this to a random secure key

# ========================================
# GOOGLE SHEETS CONFIGURATION
# ========================================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
print(f"Service Account Email: {creds.service_account_email}")
client = gspread.authorize(creds)

# TODO: Update this with your Google Sheet ID
SHEET_ID = "1hpkKB_wtU38MXC-eXWOCg0J9CSBaxuOvJnPAqEpMdzQ"
spreadsheet = client.open_by_key(SHEET_ID)


# ========================================
# ROUTES
# ========================================

@app.route("/")
def home():
    """Landing page - Email verification"""
    return render_template("index_email.html")


@app.route("/check_email", methods=["POST"])
def check_email():
    """Check if email exists in Google Sheets"""
    email = request.json.get("email", "").strip().lower()

    TARGET_COLUMN = "EMAIL ID USED IN GOETHE-ZENTRUM TVM"

    for worksheet in spreadsheet.worksheets():
        rows = worksheet.get_all_records()

        for row in rows:
            cell_value = str(row.get(TARGET_COLUMN, "")).strip().lower()

            if cell_value == email:
                # Store email and user data in session
                session["email"] = email
                # session["user_data"] = row
                session["verified"] = True

                return jsonify({
                    "found": True,
                    "sheet": worksheet.title,
                    "data": row
                })

    return jsonify({"found": False})


@app.route("/module", methods=["GET", "POST"])
def module_page():
    """Module selection page - requires email verification"""
    # Check if email is verified
    if session.get("verified"):
        print("Not verified!")
        return redirect("/")

    if request.method == "POST":
        module = request.form.get("module").strip().lower()
        session["module"] = module
        return redirect("/choose-offer")

    return render_template("module.html")


@app.route("/choose-offer")
def choose_offer():
    """Choose between Wheel or Scratch card"""
    if session.get("verified") or not session.get("module"):
        return redirect("/")

    return render_template("choose_offer.html")


@app.route("/wheel")
def wheel():
    """Spin wheel page"""
    if session.get("verified") or not session.get("module"):
        return redirect("/")

    return render_template("index.html")


@app.route("/scratch")
def scratch():
    """Scratch card page"""
    if session.get("verified") or not session.get("module"):
        return redirect("/")

    return render_template("scratch.html")


@app.route("/spin")
def spin():
    """API endpoint for wheel spin"""
    if session.get("verified"):
        return jsonify({"error": "Not authorized"}), 403

    module = session.get("module", "").lower()

    sprechen_offers = [
        "5% Discount",
        "8% Discount",
        "10% Discount",
        "12% Discount",
        "13% Discount",
        "15% Discount",
        "Next Registration 50% Discount",
        "Registration for ₹1800",
        "Registration for ₹1700"
    ]

    other_offers = [
        "10% Discount",
        "20% Discount",
        "15% Discount",
        "Next Registration 50% Discount",
        "Registration for ₹1200",
        "Registration for ₹1300",
        "Registration for ₹1400"
    ]

    if "sprechen" in module:
        offers = sprechen_offers
        base_price = 2000
    else:
        offers = other_offers
        base_price = 1500

    index = random.randint(0, len(offers) - 1)

    return jsonify({
        "offers": offers,
        "index": index,
        "module": module,
        "base_price": base_price,
        "email": session.get("email")
    })


@app.route("/scratch-reveal", methods=["POST"])
def scratch_reveal():
    """API endpoint for scratch card reveal"""
    if session.get("verified"):
        return jsonify({"error": "Not authorized"}), 403

    module = session.get("module", "").lower()

    sprechen_offers = [
        "5% Discount",
        "8% Discount",
        "10% Discount",
        "12% Discount",
        "13% Discount",
        "15% Discount",
        "Next Registration 50% Discount",
        "Registration for ₹1800",
        "Registration for ₹1700"
    ]

    other_offers = [
        "10% Discount",
        "20% Discount",
        "15% Discount",
        "Next Registration 50% Discount",
        "Registration for ₹1200",
        "Registration for ₹1300",
        "Registration for ₹1400"
    ]

    if "sprechen" in module:
        offers = sprechen_offers
        base_price = 2000
    else:
        offers = other_offers
        base_price = 1500

    reward = random.choice(offers)

    return jsonify({
        "reward": reward,
        "module": module,
        "base_price": base_price,
        "email": session.get("email")
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)