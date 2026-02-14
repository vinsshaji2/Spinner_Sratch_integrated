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

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    print(f"Service Account Email: {creds.service_account_email}")
    client = gspread.authorize(creds)

    # TODO: Update this with your Google Sheet ID
    SHEET_ID = "1hpkKB_wtU38MXC-eXWOCg0J9CSBaxuOvJnPAqEpMdzQ"
    spreadsheet = client.open_by_key(SHEET_ID)
    print(f"Successfully connected to Google Sheet: {spreadsheet.title}")
except FileNotFoundError:
    print("ERROR: service_account.json not found!")
    print("Please add your Google Sheets service account credentials file.")
    spreadsheet = None
except Exception as e:
    print(f"ERROR connecting to Google Sheets: {e}")
    spreadsheet = None


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
    try:
        # Check if spreadsheet is connected
        if spreadsheet is None:
            print("ERROR: Google Sheets not connected")
            return jsonify({"error": "Database connection error. Please contact support."}), 500

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
            try:
                # Get all values from the worksheet
                all_values = worksheet.get_all_values()

                # Skip empty worksheets
                if not all_values or len(all_values) < 2:
                    continue

                # Get header row
                headers = all_values[0]

                # Find the target column index
                try:
                    target_col_index = headers.index(TARGET_COLUMN)
                except ValueError:
                    # Column not found in this worksheet, skip it
                    continue

                # Check each row (skip header)
                for row_values in all_values[1:]:
                    # Make sure row has enough columns
                    if len(row_values) > target_col_index:
                        cell_value = str(row_values[target_col_index]).strip().lower()

                        if cell_value == email:
                            # Email found in spreadsheet - already registered
                            # Create a dict of the row data
                            row_data = {}
                            for i, header in enumerate(headers):
                                if i < len(row_values):
                                    row_data[header] = row_values[i]

                            return jsonify({
                                "found": True,
                                "sheet": worksheet.title,
                                "data": row_data
                            })

            except Exception as worksheet_error:
                # Log the error but continue checking other worksheets
                print(f"Error processing worksheet {worksheet.title}: {worksheet_error}")
                continue

        # Email not found - proceed with registration
        # Store user data in session
        session["email"] = email
        session["name"] = name
        session["phone"] = phone
        session["verified"] = True

        return jsonify({"found": False})

    except Exception as e:
        print(f"Error in check_email: {e}")
        return jsonify({"error": "An error occurred while checking email. Please try again."}), 500


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