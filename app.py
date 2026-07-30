from flask import Flask, jsonify, render_template_string, send_file, send_from_directory
import os
import pandas as pd

app = Flask(__name__)

def ensure_data():
    if not os.path.exists('Automated_Report.xlsx') or not os.path.exists('monthly_sales.png'):
        try:
            if not os.path.exists('raw_sales_data.csv'):
                import generate_data
                generate_data.main()
            import data_pipeline
            data_pipeline.run_pipeline()
        except Exception as e:
            print("Error running data pipeline:", e)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automated Data Cleaning & Reporting Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero { background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); color: white; padding: 2.5rem 0; margin-bottom: 2rem; }
        .card { border: none; border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
        .card-header { background-color: white; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b; }
        .metric-value { font-size: 2rem; font-weight: bold; color: #2563eb; }
        .metric-label { font-size: 0.9rem; color: #64748b; }
    </style>
</head>
<body>
    <div class="hero text-center">
        <div class="container">
            <h1 class="display-5 fw-bold">Data Cleaning & Reporting Automation</h1>
            <p class="lead mb-0">Automated ETL Pipeline, Data Cleaning & Monthly Reporting</p>
        </div>
    </div>

    <div class="container">
        <div class="row text-center mb-4">
            <div class="col-md-4">
                <div class="card p-3">
                    <div class="metric-label">Total Cleaned Revenue</div>
                    <div class="metric-value">${{ "{:,.2f}".format(total_revenue) }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <div class="metric-label">Total Orders Processed</div>
                    <div class="metric-value">{{ total_orders }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <div class="metric-label">Top Performing Product</div>
                    <div class="metric-value text-emerald-600 fs-4">{{ top_product }}</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Monthly Revenue Trend</div>
                    <div class="card-body text-center">
                        <img src="/monthly_sales.png" class="img-fluid rounded" alt="Monthly Sales Chart" onerror="this.src='https://via.placeholder.com/700x400?text=Chart+Generating...'">
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">Export & API</div>
                    <div class="card-body">
                        <p class="text-muted small">Download automated Excel report or access raw JSON endpoints.</p>
                        <a href="/download/report" class="btn btn-success w-100 mb-2">📥 Download Excel Report</a>
                        <a href="/api/data" class="btn btn-outline-primary w-100" target="_blank">🔗 Raw JSON API</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ensure_data()
    total_revenue, total_orders, top_product = 0.0, 0, "N/A"
    try:
        import data_pipeline
        df = data_pipeline.load_data()
        if df is not None:
            df_clean = data_pipeline.clean_data(df)
            total_revenue = df_clean['Revenue'].sum()
            total_orders = len(df_clean)
            top_product = df_clean.groupby('Product')['Revenue'].sum().idxmax()
    except Exception as e:
        print("Error serving index:", e)

    return render_template_string(HTML_TEMPLATE, total_revenue=total_revenue, total_orders=total_orders, top_product=top_product)

@app.route('/api/data')
def api_data():
    ensure_data()
    try:
        import data_pipeline
        df = data_pipeline.load_data()
        if df is not None:
            df_clean = data_pipeline.clean_data(df)
            df_clean['Month'] = df_clean['Month'].astype(str)
            df_clean['Date'] = df_clean['Date'].astype(str)
            return jsonify(df_clean.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Data not available"}), 404

@app.route('/monthly_sales.png')
def serve_chart():
    ensure_data()
    if os.path.exists('monthly_sales.png'):
        return send_file('monthly_sales.png', mimetype='image/png')
    return "Chart missing", 404

@app.route('/download/report')
def download_report():
    ensure_data()
    if os.path.exists('Automated_Report.xlsx'):
        return send_file('Automated_Report.xlsx', as_attachment=True, download_name='Automated_Report.xlsx')
    return "Report missing", 404

if __name__ == '__main__':
    ensure_data()
    app.run(debug=True, port=5000)
