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
    """Landing page - Email verification with name and phone"""
    return render_template("index_email.html")


@app.route("/check_email", methods=["POST"])
def check_email():
    """Check if email exists in Google Sheets and store user info"""
    data = request.json
    email = data.get("email", "").strip().lower()
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    terms_accepted = data.get("terms_accepted", False)

    # Validate all fields
    if not all([email, name, phone, terms_accepted]):
        return jsonify({"error": "All fields are required and terms must be accepted"}), 400

    TARGET_COLUMN = "EMAIL ID USED IN GOETHE-ZENTRUM TVM"

    for worksheet in spreadsheet.worksheets():
        rows = worksheet.get_all_records()

        for row in rows:
            cell_value = str(row.get(TARGET_COLUMN, "")).strip().lower()

            if cell_value == email:
                # Email found in spreadsheet - already registered
                return jsonify({
                    "found": True,
                    "sheet": worksheet.title,
                    "data": row
                })

    # Email not found - proceed with registration
    # Store user data in session
    session["email"] = email
    session["name"] = name
    session["phone"] = phone
    session["verified"] = True

    return jsonify({"found": False})


@app.route("/module", methods=["GET", "POST"])
def module_page():
    """Module selection page - requires email verification"""
    # Check if email is verified
    if not session.get("verified"):
        print("Not verified!")
        return redirect("/")

    if request.method == "POST":
        module = request.form.get("module").strip()
        session["module"] = module
        return redirect("/choose-offer")

    return render_template("module.html")


@app.route("/choose-offer")
def choose_offer():
    """Choose between Wheel or Scratch card"""
    if not session.get("verified") or not session.get("module"):
        return redirect("/")

    return render_template("choose_offer.html")


@app.route("/wheel")
def wheel():
    """Spin wheel page"""
    if not session.get("verified") or not session.get("module"):
        return redirect("/")

    return render_template("index.html")


@app.route("/scratch")
def scratch():
    """Scratch card page"""
    if not session.get("verified") or not session.get("module"):
        return redirect("/")

    return render_template("scratch.html")


@app.route("/spin")
def spin():
    """API endpoint for wheel spin"""
    if not session.get("verified"):
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
        "email": session.get("email"),
        "name": session.get("name"),
        "phone": session.get("phone")
    })


@app.route("/scratch-reveal", methods=["POST"])
def scratch_reveal():
    """API endpoint for scratch card reveal"""
    if not session.get("verified"):
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
        "email": session.get("email"),
        "name": session.get("name"),
        "phone": session.get("phone")
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)