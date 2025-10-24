from datetime import datetime
from tabulate import tabulate
from fastapi.responses import HTMLResponse
# Overall system health


def overall_check(results, fig):
    # Create color-coded HTML table
    table_html = """
    <table style="margin: 20px auto; border-collapse: collapse;">
    <tr><th style='padding:8px 16px; background:#e9ecef;'>Node</th>
    <th style='padding:8px 16px; background:#e9ecef;'>Status</th></tr>
    """
    for node, ok in results.items():
        color = "green" if ok else "red"
        status = "OK" if ok else "FAIL"
        table_html += f"<tr><td style='border:1px solid #ccc; padding:8px 16px;'>{node}</td>"
        table_html += f"<td style='border:1px solid #ccc; padding:8px 16px; color:{color}; font-weight:bold;'>{status}</td></tr>"
    table_html += "</table>"

    overall = "OK" if all(results.values()) else "FAILED"
    overall_color = "green" if overall == "OK" else "red"
    # Build Plotly visualization


    fig_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    html_report = f"""
       <html>
         <head>
           <title>DAG Health Report</title>
           <style>
             body {{ font-family: Arial, sans-serif; background: #f8f9fa; margin: 0; padding: 20px; }}
             h1 {{ text-align: center; color: {overall_color}; }}
             h2 {{ text-align: center; }}
             table {{ margin: 20px auto; border-collapse: collapse; }}
             th, td {{ border: 1px solid #ccc; padding: 8px 16px; }}
             th {{ background-color: #e9ecef; }}
             .container {{ text-align: center; }}
           </style>
         </head>
         <body>
           <h1>Overall System Health: {overall}</h1>
           <h3 style="text-align:center; color:#666;">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h3>
           <div class="container">
             <h2>Health Table</h2>
             {table_html}
             <h2>DAG Visualization</h2>
             {fig_html}
           </div>
         </body>
       </html>
       """
    # Save locally for easy viewing
    with open("dag_report.html", "w") as f:
        f.write(html_report)

    print("HTML report saved locally as dag_report.html")
    return HTMLResponse(content=html_report)
