from flask import Flask, render_template_string, request from datetime import datetime

app = Flask(name)

HTML_TEMPLATE = ''' <!doctype html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Overtime Calculator</title>
    <style>
        body { font-family: sans-serif; margin: 30px; }
        input, button { padding: 5px; margin: 5px 0; width: 100%; }
        label { font-weight: bold; }
    </style>
</head>
<body>
    <h2>Overtime Calculator</h2>
    <form method="POST">
        <label>Work Time (e.g. 09:00 - 15:00)</label>
        <input name="work_time" required>
        <label>Contracted Time (e.g. 06:00 - 09:00, 15:15 - 19:30)</label>
        <input name="contracted_time" required>
        <button type="submit">Calculate Overtime</button>
    </form>
    {% if result %}
        <h3>Result</h3>
        <p>{{ result }}</p>
    {% endif %}
</body>
</html>
'''def parse_time_range(time_range): try: start_str, end_str = time_range.split('-') start = datetime.strptime(start_str.strip(), '%H:%M') end = datetime.strptime(end_str.strip(), '%H:%M') return (start, end) except: return None

def calculate_overtime(work_str, contract_str): work_range = parse_time_range(work_str) contract_parts = contract_str.split(',') contract_ranges = [parse_time_range(part) for part in contract_parts if parse_time_range(part)]

if not work_range or not contract_ranges:
    return "Invalid time format."

work_start, work_end = work_range
total_work_minutes = (work_end - work_start).total_seconds() / 60

total_contracted_minutes = 0
for start, end in contract_ranges:
    total_contracted_minutes += (end - start).total_seconds() / 60

overtime_minutes = max(0, total_work_minutes - total_contracted_minutes)
hours = int(overtime_minutes // 60)
minutes = int(overtime_minutes % 60)
return f"Overtime: {hours}h {minutes}m"

@app.route('/', methods=['GET', 'POST']) def home(): result = None if request.method == 'POST': work_time = request.form['work_time'] contracted_time = request.form['contracted_time'] result = calculate_overtime(work_time, contracted_time) return render_template_string(HTML_TEMPLATE, result=result)

if name == 'main': app.run(debug=True)

