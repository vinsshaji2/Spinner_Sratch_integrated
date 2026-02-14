# Goethe-Zentrum Registration & Gamification System

A Flask-based web application for managing Goethe-Zentrum exam registrations with gamified offer reveals (Spin the Wheel & Scratch Card).

## Features

### 1. **User Registration**
- Collects full name, phone number, and email address
- Validates email against Google Sheets database
- Mandatory Terms & Conditions acceptance
- Prevents duplicate registrations

### 2. **Module Selection**
- Multiple module selection (Sprechen, Lesen, Hören, Schreiben)
- Comma-separated module storage
- Different pricing based on modules

### 3. **Gamified Offer Reveal**
- **Spin the Wheel**: Interactive spinning wheel animation
- **Scratch Card**: Interactive scratch-to-reveal card
- Session-based one-time use (prevents multiple attempts)

### 4. **WhatsApp Integration**
- Automatic message generation with:
  - User details (Name, Phone, Email)
  - Selected modules
  - Offer details
  - Price calculations
  - Discount savings

## Installation

### Prerequisites
- Python 3.7+
- Google Sheets API credentials
- Flask and dependencies

### Setup Steps

1. **Clone or extract the application**
```bash
cd goethe-app
```

2. **Install dependencies**
```bash
pip install flask gspread oauth2client
```

3. **Configure Google Sheets**
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create Service Account and download `service_account.json`
   - Place `service_account.json` in the project root
   - Share your Google Sheet with the service account email
   - Update `SHEET_ID` in `app.py` (line 26)

4. **Update WhatsApp Number**
   - In `static/wheel.js` (line 229): Update `academyNumber`
   - In `static/scratch.js` (line 194): Update `academyNumber`

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
   - Open browser to `http://localhost:5000`

## File Structure

```
goethe-app/
├── app.py                          # Main Flask application
├── service_account.json            # Google Sheets credentials (not included)
├── templates/
│   ├── index_email.html           # Registration page with T&C
│   ├── module.html                # Module selection page
│   ├── choose_offer.html          # Choose Wheel or Scratch
│   ├── index.html                 # Spin the Wheel page
│   └── scratch.html               # Scratch Card page
└── static/
    ├── style.css                  # Wheel page styles
    ├── scratch.css                # Scratch card styles
    ├── wheel.js                   # Wheel logic
    └── scratch.js                 # Scratch card logic
```

## Configuration

### Google Sheets Format
Your Google Sheet should have a column named:
```
EMAIL ID USED IN GOETHE-ZENTRUM TVM
```

### Offers Configuration
Edit the offers in `app.py`:

**For Sprechen modules** (lines 116-124):
```python
sprechen_offers = [
    "5% Discount",
    "8% Discount",
    # ... add more offers
]
```

**For other modules** (lines 126-132):
```python
other_offers = [
    "10% Discount",
    "20% Discount",
    # ... add more offers
]
```

### Pricing
- **Sprechen**: ₹2000 (base price)
- **Other modules**: ₹1500 (base price)

Update in `app.py` lines 135-139.

## Terms & Conditions

The application includes comprehensive T&C covering:
- Cancellation Policy
- Payment Policy (₹1500/₹2000)
- Account & Registration Policy
- Exam Fee Structure (₹6,254 per module or ₹25,016 for all)

Edit the terms in `templates/index_email.html` (lines 176-218).

## Session Management

- Uses Flask sessions to store user data
- Browser sessionStorage for wheel/scratch one-time use
- Prevents multiple spins/scratches per session

## Security Notes

1. Change `SECRET_KEY` in `app.py` (line 8) to a secure random string
2. Keep `service_account.json` secure and never commit to version control
3. Validate all user inputs server-side
4. Use HTTPS in production

## Customization

### Colors & Branding
- Edit CSS files in `static/` folder
- Update gradients, colors, and fonts
- Modify emoji icons

### WhatsApp Message Format
- Edit in `wheel.js` (lines 176-198)
- Edit in `scratch.js` (lines 141-163)

### Animation Timing
- Wheel spin duration: `wheel.js` line 53
- Scratch reveal threshold: `scratch.js` line 132

## Troubleshooting

### Common Issues

1. **Google Sheets not connecting**
   - Verify service account email has access to sheet
   - Check SHEET_ID is correct
   - Ensure API is enabled in Google Cloud Console

2. **Session errors**
   - Check SECRET_KEY is set
   - Clear browser cookies/cache

3. **WhatsApp not opening**
   - Verify phone number format (no spaces, include country code)
   - Check URL encoding

## Support

For issues or questions, contact:
- Phone: +91 7034942438
- Update support contact in templates as needed

## License

Proprietary - Deutsch Zeit / Goethe-Zentrum TVM