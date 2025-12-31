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
        'password', 'password123', '123456', '12345678', '123456789','1234567890','password1234',
        'qwerty', 'abc123', 'monkey', '1234567', 'letmein', 'trustno1',
        'dragon', 'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321', 'superman',
        'qazwsx', 'michael', 'football', 'welcome', 'jesus', 'ninja',
        'mustang', 'password1', '123qwe', 'admin', 'login', 'access',
        'root', 'toor', 'pass', 'test', 'guest', 'info', 'adm',
        'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
    ]

    def __init__(self):
        self.min_length = 10

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

        # 1.5 Contains Common Word
        contains_common = False
        found_common = ""
        for common in self.COMMON_PASSWORDS:
            if len(common) >= 5 and common in password_lower:
                contains_common = True
                found_common = common
                break
        
        checks.append({
            'name': 'Contains Common Word',
            'passed': not contains_common,
            'message': f"Contains common word '{found_common}'" if contains_common else "No common words found"
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

        # 5. Sequential Patterns
        sequences = [
            '01234567890',
            'abcdefghijklmnopqrstuvwxyz',
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
        ]
        max_seq_len = 0
        
        for seq in sequences:
            for direction in [seq, seq[::-1]]:
                for i in range(len(password_lower)):
                    for j in range(i + 3, len(password_lower) + 1):
                        chunk = password_lower[i:j]
                        if chunk in direction:
                            max_seq_len = max(max_seq_len, len(chunk))
                            
        has_sequence = max_seq_len >= 4
        checks.append({
            'name': 'Sequential Patterns',
            'passed': not has_sequence,
            'message': f"Contains sequence of {max_seq_len} characters" if has_sequence else "No sequential patterns",
            'metadata': {'max_seq_len': max_seq_len}
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
            elif check['name'] == 'Contains Common Word':
                score -= 30
            elif check['name'] == 'No Repetition':
                score -= 10
            elif check['name'] == 'Sequential Patterns':
                seq_len = check.get('metadata', {}).get('max_seq_len', 0)
                if seq_len >= 4:
                    score -= (seq_len * 5)
        
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
        
        # Filter out backend-only checks for UI
        ui_checks = [c for c in checks if c['name'] != 'Contains Common Word']
        
        # Recommendations
        recommendations = []
        failed_ui = [c for c in ui_checks if not c['passed']]
        
        if not failed_ui and score > 80:
            recommendations.append("Excellent password hygiene!")
        else:
            for c in failed_ui:
                if c['name'] == 'Common Password': recommendations.append("Choose a unique password.")
                if c['name'] == 'Length': recommendations.append(f"Increase length to at least {self.min_length}.")
                if c['name'] == 'No Repetition': recommendations.append("Avoid repeating characters.")
                if c['name'] == 'Sequential Patterns': recommendations.append("Avoid sequential characters (e.g. '123', 'abc').")
            
            # Add variety recommendations if score is low and no specific failures
            if score < 70 and not failed_ui:
                 recommendations.append("Add a mix of uppercase, numbers, and special characters.")

        return {
            'password': password,
            'risk_score': score,
            'risk_level': strength['label'],
            'risk_color': strength['color'],
            'checks': ui_checks,
            'issues': [c['message'] for c in failed_ui],
            'issue_count': len(failed_ui),
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
