with open('frontend/landing.html', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        for k in ['id="planes"', 'id="calculadora"', '<script>', '<script', 'updateBilling', 'calcBudget']:
            if k in line:
                print(f'{i+1}: {line.strip()[:100]}')
