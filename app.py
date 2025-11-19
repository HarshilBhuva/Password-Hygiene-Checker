from flask import Flask, render_template, request, jsonify
import re
import string
from typing import Dict, List, Tuple, Any

app = Flask(__name__)

class PasswordChecker:
    """
    Password Hygiene Checker using Simplified Heuristic Analysis.
    """
    
    COMMON_PASSWORDS = [
        'password', 'password123', '123456', '12345678', '123456789','1234567890',
        'qwerty', 'abc123', 'monkey', '1234567', 'letmein', 'trustno1',
        'dragon', 'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321', 'superman',
        'qazwsx', 'michael', 'football', 'welcome', 'jesus', 'ninja',
        'mustang', 'password1', '123qwe', 'admin', 'login', 'access',
        'root', 'toor', 'pass', 'test', 'guest', 'info', 'adm',
        'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
    ]

    def __init__(self):
        self.min_length = 8

    def check_patterns(self, password: str) -> List[Dict[str, Any]]:
        """
        Run comprehensive pattern checks.
        """
        checks = []
        password_lower = password.lower()
        
        # 1. Common Password
        is_common = password_lower in self.COMMON_PASSWORDS
        checks.append({
            'name': 'Common Password',
            'passed': not is_common,
            'message': "Password is too common" if is_common else "Not a common password"
        })

        # 2. Length
        checks.append({
            'name': 'Length',
            'passed': len(password) >= self.min_length,
            'message': f"Minimum {self.min_length} characters" if len(password) < self.min_length else "Length requirement met"
        })
        
        # 3. Character Types
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(f'[{re.escape(string.punctuation)}]', password))
        
        checks.append({'name': 'Uppercase', 'passed': has_upper, 'message': "Contains uppercase" if has_upper else "Missing uppercase"})
        checks.append({'name': 'Lowercase', 'passed': has_lower, 'message': "Contains lowercase" if has_lower else "Missing lowercase"})
        checks.append({'name': 'Digits', 'passed': has_digit, 'message': "Contains digits" if has_digit else "Missing digits"})
        checks.append({'name': 'Special Characters', 'passed': has_special, 'message': "Contains special chars" if has_special else "Missing special chars"})

        # 4. No Repetition
        max_repeat = 2
        has_repeats = False

        if len(password) > 3:
            for char in set(password):
                if char * (max_repeat + 1) in password:
                    has_repeats = True
                    break
        
        checks.append({
            'name': 'No Repetition',
            'passed': not has_repeats,
            'message': "Too many repeated characters" if has_repeats else "No excessive repetition"
        })

        return checks

    def calculate_score(self, password: str, checks: List[Dict[str, Any]]) -> int:
        """
        Calculate score (0-100) based on simple heuristics.
        """
        score = 0
        score += min(40, len(password) * 4)
        
        types_present = 0
        if re.search(r'[a-z]', password): types_present += 1
        if re.search(r'[A-Z]', password): types_present += 1
        if re.search(r'\d', password): types_present += 1
        if re.search(f'[{re.escape(string.punctuation)}]', password): types_present += 1
        
        score += types_present * 15
        
        # Penalties
        failed_checks = [c for c in checks if not c['passed']]
        for check in failed_checks:
            if check['name'] == 'Common Password':
                return 0 # Immediate fail
            elif check['name'] == 'No Repetition':
                score -= 10
        
        return int(max(0, min(100, score)))

    def get_strength_label(self, score: int) -> Dict[str, str]:
        if score < 30: return {"label": "Very Weak", "color": "#ff0055"}
        if score < 50: return {"label": "Weak", "color": "#ffb700"}
        if score < 70: return {"label": "Moderate", "color": "#ff8800"}
        if score < 90: return {"label": "Strong", "color": "#00ff9d"}
        return {"label": "Very Strong", "color": "#00d4ff"}

    def check_password(self, password: str) -> Dict[str, Any]:
        checks = self.check_patterns(password)
        score = self.calculate_score(password, checks)
        strength = self.get_strength_label(score)
        
        # Recommendations
        recommendations = []
        failed = [c for c in checks if not c['passed']]
        if not failed and score > 80:
            recommendations.append("Excellent password hygiene!")
        else:
            for c in failed:
                if c['name'] == 'Common Password': recommendations.append("Choose a unique password.")
                if c['name'] == 'Length': recommendations.append(f"Increase length to at least {self.min_length}.")
                if c['name'] == 'No Repetition': recommendations.append("Avoid repeating characters.")
            
            # Add variety recommendations if score is low and no specific failures
            if score < 70 and not failed:
                 recommendations.append("Add a mix of uppercase, numbers, and special characters.")

        return {
            'password': password,
            'risk_score': score,
            'risk_level': strength['label'],
            'risk_color': strength['color'],
            'checks': checks,
            'issues': [c['message'] for c in failed],
            'issue_count': len(failed),
            'recommendations': recommendations,
            'valid': score >= 50
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    try:
        data = request.get_json()
        password = data.get('password', '').strip()
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
            
        checker = PasswordChecker()
        result = checker.check_password(password)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
