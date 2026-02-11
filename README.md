# 🎯 Goethe-Zentrum Complete Integrated System

## ✨ Features

This integrated system combines:
1. **Email Verification** - Validates users against Google Sheets database
2. **Module Selection** - Users choose their German course module
3. **Dual Reward System** - Choose between Spin Wheel or Scratch Card
4. **WhatsApp Integration** - Direct messaging with offer details
5. **Session Management** - Prevents multiple plays per session

---

## 📁 Project Structure

```
goethe-integrated/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── service_account.json            # Google Sheets credentials (INCLUDED)
│
├── templates/                      # HTML templates
│   ├── index_email.html           # Email verification page
│   ├── module.html                # Module selection page
│   ├── choose_offer.html          # Choose reward method
│   ├── index.html                 # Spin wheel page
│   └── scratch.html               # Scratch card page
│
└── static/                        # Static files (CSS & JS)
    ├── style.css                  # Wheel styling
    ├── wheel.js                   # Wheel logic
    ├── scratch.css                # Scratch card styling
    └── scratch.js                 # Scratch card logic
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**OR install individually:**

```bash
pip install Flask==3.0.0 gspread==5.11.3 oauth2client==4.1.3
```

### Step 2: Configure Google Sheet

Your service account is already included (`service_account.json`).

**IMPORTANT:** Share your Google Sheet with this email:
```
sheet-bot@plasma-winter-482304-r7.iam.gserviceaccount.com
```

**How to share:**
1. Open your Google Sheet
2. Click "Share" button
3. Paste the email above
4. Give **"Editor"** access
5. Click "Send"

### Step 3: Update Configuration

**🔧 IN `app.py` (Line 24):**

Your current Sheet ID is already set:
```python
SHEET_ID = "1hpkKB_wtU38MXC-eXWOCg0J9CSBaxuOvJnPAqEpMdzQ"
```

If you want to use a different Google Sheet, replace it with your Sheet ID.

**📱 IN `static/wheel.js` (Line 204):**

```javascript
const academyNumber = "917034942438";  // ← CHANGE THIS
```

**📱 IN `static/scratch.js` (Line 213):**

```javascript
const academyNumber = "917034942438";  // ← CHANGE THIS
```

Replace `917034942438` with your WhatsApp number (include country code, no + or spaces).

### Step 4: Run the Application

```bash
python app.py
```

The app will start at: **http://localhost:5000**

---

## 🎮 Complete User Flow

```
1. User visits homepage (/)
   ↓
2. Enters email address
   ↓
3. System checks Google Sheets
   ↓
4. If found → Proceed to Module Selection
   If not found → Show error
   ↓
5. User selects module (Sprechen, Lesen, Hören, or Schreiben)
   ↓
6. Choose reward method (Spin Wheel or Scratch Card)
   ↓
7. Play the game and win an offer
   ↓
8. Send result to WhatsApp
```

---

## 📊 Google Sheet Requirements

Your Google Sheet **MUST** have this exact column name:

```
EMAIL ID USED IN GOETHE-ZENTRUM TVM
```

Example sheet structure:

| EMAIL ID USED IN GOETHE-ZENTRUM TVM | Name    | Phone      | Other... |
|-------------------------------------|---------|------------|----------|
| john@example.com                    | John    | 1234567890 | ...      |
| jane@example.com                    | Jane    | 0987654321 | ...      |

**⚠️ IMPORTANT:**
- Column name must match exactly (case-sensitive)
- The system will search through ALL worksheets in your spreadsheet
- Emails are compared case-insensitively

---

## 💰 Offer Configuration

### For Sprechen Module (₹2000 base price):
- 10% Discount
- 20% Discount
- 15% Discount
- Next Registration 50% Discount
- Exam Tips
- Registration for ₹1500

### For Other Modules (₹1500 base price):
- 10% Discount
- 20% Discount
- 15% Discount
- Next Registration 50% Discount
- Exam Tips
- Registration for ₹1000
- Registration for ₹1200

**To modify offers, edit `app.py` lines 66-92.**

---

## 🔒 Security Features

✅ Session-based authentication
✅ Email verification required before access
✅ Protected routes (can't skip verification)
✅ One play per session (stored in sessionStorage)
✅ Server-side randomization (client can't cheat)

---

## 🛠️ Troubleshooting

### "Module not found" errors

```bash
pip install Flask gspread oauth2client
```

### "Permission denied" with Google Sheets

1. Check you shared the sheet with: `sheet-bot@plasma-winter-482304-r7.iam.gserviceaccount.com`
2. Ensure the service account has **"Editor"** permissions
3. Verify the `SHEET_ID` in `app.py` is correct

### Email not being found

1. Check column name is exactly: `EMAIL ID USED IN GOETHE-ZENTRUM TVM`
2. Verify the email exists in your sheet
3. The system searches all worksheets - make sure email is in one of them

### WhatsApp not opening

1. Make sure you updated the `academyNumber` in both:
   - `static/wheel.js` (line 204)
   - `static/scratch.js` (line 213)
2. Number format: `91XXXXXXXXXX` (country code + number, no spaces)

### Session issues / Can't replay

Clear browser data or use incognito mode. Sessions are stored in:
- Server-side: Flask session
- Client-side: sessionStorage

---

## 📱 WhatsApp Message Format

When user wins, the WhatsApp message includes:

```
🎉 Spin & Win Result!

Module: Sprechen
Offer: 20% Discount
Base Price: ₹2000
Final Amount: ₹1600
(Saved ₹400!)

Email: user@example.com

I'd like to book this offer!
```

---

## 🎨 Customization

### Change Colors

**Email page:** Edit `templates/index_email.html` (lines 20-21)
**Module page:** Edit `templates/module.html` (line 16)
**Wheel page:** Edit `static/style.css` (line 11)
**Scratch page:** Edit `static/scratch.css` (line 11)

### Change Offers

Edit `app.py` function `spin()` (lines 66-92) and `scratch_reveal()` (lines 107-133)

### Modify Base Prices

In `app.py`:
- Sprechen: Line 78
- Other modules: Line 82

---

## 🔐 Change Secret Key

In `app.py` line 8:

```python
app.config["SECRET_KEY"] = "super_secret_key_123"  # ← Change this
```

Generate a secure random key:

```python
import secrets
print(secrets.token_hex(32))
```

---

## 📝 Routes Reference

| Route              | Method | Description                    | Requires Auth |
|--------------------|--------|--------------------------------|---------------|
| `/`                | GET    | Email verification page        | No            |
| `/check_email`     | POST   | Validate email in Google Sheet | No            |
| `/module`          | GET    | Module selection page          | Yes           |
| `/module`          | POST   | Save module selection          | Yes           |
| `/choose-offer`    | GET    | Choose reward method           | Yes           |
| `/wheel`           | GET    | Spin wheel page                | Yes           |
| `/scratch`         | GET    | Scratch card page              | Yes           |
| `/spin`            | GET    | Get wheel spin result          | Yes           |
| `/scratch-reveal`  | POST   | Get scratch card result        | Yes           |

---

## 🎯 What You Need to Change

### MANDATORY (Must change before deploying):

1. **WhatsApp Number** (2 places):
   - `static/wheel.js` line 204
   - `static/scratch.js` line 213

2. **Google Sheet Sharing**:
   - Share with: `sheet-bot@plasma-winter-482304-r7.iam.gserviceaccount.com`

3. **Secret Key** (for production):
   - `app.py` line 8

### OPTIONAL (Can keep as-is):

1. **Google Sheet ID**: Already configured for your sheet
2. **Offers**: Can modify in `app.py`
3. **Colors/Styling**: Can customize CSS files
4. **Base Prices**: Can adjust in `app.py`

---

## ✅ Pre-Flight Checklist

Before running:

- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Shared Google Sheet with service account email
- [ ] Updated WhatsApp number in `wheel.js`
- [ ] Updated WhatsApp number in `scratch.js`
- [ ] Verified Google Sheet has correct column name
- [ ] (Optional) Changed secret key for production

---

## 🚀 Deployment

For production deployment:

1. Change `debug=True` to `debug=False` in `app.py` line 144
2. Use a production WSGI server like **Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. Set up SSL certificate for HTTPS
4. Use environment variables for secrets
5. Consider using a reverse proxy like Nginx

---

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all configuration steps are completed
3. Check console logs for error messages
4. Ensure Google Sheets API is accessible

---

## 🎉 You're All Set!

Run `python app.py` and visit **http://localhost:5000**

Enjoy your integrated Goethe-Zentrum Spin & Win system! 🎯