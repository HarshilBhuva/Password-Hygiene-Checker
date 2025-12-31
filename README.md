# Password Hygiene Checker

A simple web application to check password strength and security. This tool analyzes various factors including password length, character variety, patterns, and common weak passwords to determine the strength level.

## Features

- ✅ Password length validation (minimum 10 characters)
- ✅ Character variety checks (uppercase, lowercase, digits, special characters)
- ✅ Common weak password detection
- ✅ Pattern detection (repeated characters)
- ✅ Strength scoring system (Very Weak, Weak, Moderate, Strong, Very Strong)
- ✅ Modern, responsive UI
- ✅ Detailed recommendations for improvement


## Installation

### Quick Start

1. **Clone or download this repository**

2. **Run the setup script:**
   ```bash
   setup.bat
   ```

This will automatically create a virtual environment and install all dependencies.

### Manual Installation

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Easy Way (Using Run Script)

```bash
run.bat
```

### Manual Way

1. **Activate the virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

2. **Run the Flask application:**
   ```bash
   python app.py
   ```

3. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```
    OR 
      ```
      http://127.0.0.1:5000/
      ```

4. **Enter a password to check** in the input field and click "Check Password"

5. **Review the results:**
   - Strength level (Very Weak, Weak, Moderate, Strong, Very Strong)
   - Strength score (0-100)
   - Detailed checks performed
   - List of issues found
   - Recommendations for improvement

## Strength Levels

- **VERY WEAK (0-29)**: Password fails basic security requirements
- **WEAK (30-49)**: Password has significant security flaws
- **MODERATE (50-69)**: Password meets basic requirements but could be improved
- **STRONG (70-89)**: Password is well-constructed and secure
- **VERY STRONG (90-100)**: Password demonstrates excellent security practices

## How It Works

The checker analyzes passwords based on:

1. **Length**: Validates password length (default: 10-128 characters)
2. **Character Variety**: Checks for uppercase, lowercase, digits, and special characters
3. **Common Passwords**: Flags passwords that are commonly used and easily guessable
4. **Pattern Detection**: Identifies repeated characters
5. **Strength Scoring**: Calculates a comprehensive score based on all factors

## Checks Performed

- **Length Check**: Validates password length (minimum 10 characters recommended)
- **Uppercase Letters**: Ensures presence of capital letters (A-Z)
- **Lowercase Letters**: Ensures presence of lowercase letters (a-z)
- **Digits**: Ensures presence of numbers (0-9)
- **Special Characters**: Ensures presence of special characters (!@#$%^&*, etc.)
- **Common Password Check**: Flags passwords that are commonly used and easily guessable
- **Repeated Characters**: Identifies excessive character repetition

## Limitations

⚠️ **This is a basic password hygiene checker and should be used as a guide, not the sole security measure.**

- Results are based on heuristics and pattern matching
- Some strong passwords may appear weaker due to pattern detection
- Always use unique passwords for different accounts
- Consider using a password manager for better security
- Enable two-factor authentication when available

## Requirements

- Python 3.7 or higher
- Flask

## Security Note

⚠️ **This tool runs locally on your machine. Passwords are not sent to external servers and are only processed in your browser and local Flask server.**

## License

This project is open source and available for use.
