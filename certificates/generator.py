import os
import json
from datetime import datetime
from typing import Dict, Any


def generate_wipe_certificate(
    device_info: Dict[str, Any],
    timestamp: str,
    method: str,
    hash_before: str,
    hash_after: str,
    output_dir: str,
) -> Dict[str, str]:
    """
    Generates:
    - JSON certificate
    - HTML certificate (printable)

    Returns a dict with paths:
    {
      "json": "...",
      "html": "..."
    }
    """

    cert = {
        "device_info": device_info,
        "wipe_method": method,
        "hash_before": hash_before,
        "hash_after": hash_after,
        "timestamp_utc": timestamp,
        "generated_at_utc": datetime.utcnow().isoformat() + "Z",
        "status": "SUCCESS" if hash_before != hash_after else "WARNING_HASH_MATCH",
    }

    os.makedirs(output_dir, exist_ok=True)

    # Filename base uses timestamp for uniqueness
    base_name = f"wipe_certificate_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    json_path = os.path.join(output_dir, base_name + ".json")
    html_path = os.path.join(output_dir, base_name + ".html")

    # JSON certificate
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=4)

    # HTML certificate (simple, printable)
    html_content = _render_html_certificate(cert)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return {"json": json_path, "html": html_path}


def _render_html_certificate(cert: Dict[str, Any]) -> str:
    device = cert["device_info"]
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>SecureWipe - Wipe Certificate</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}
        .card {{
            border: 1px solid #333;
            padding: 20px;
            border-radius: 8px;
            max-width: 800px;
        }}
        h1 {{
            text-align: center;
        }}
        .section-title {{
            font-weight: bold;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        td {{
            padding: 4px 8px;
            vertical-align: top;
        }}
        .label {{
            font-weight: bold;
            width: 200px;
        }}
        .status-success {{
            color: green;
            font-weight: bold;
        }}
        .status-warning {{
            color: orange;
            font-weight: bold;
        }}
    </style>
</head>
<body>
<div class="card">
    <h1>SecureWipe - Wipe Certificate</h1>
    <p>This document certifies that a secure wipe operation was performed on the following storage media.</p>

    <div class="section-title">Device Information</div>
    <table>
        <tr><td class="label">Device Type</td><td>{device.get("device_type","")}</td></tr>
        <tr><td class="label">Path</td><td>{device.get("path","")}</td></tr>
        <tr><td class="label">Size (bytes)</td><td>{device.get("size_bytes","")}</td></tr>
    </table>

    <div class="section-title">Wipe Details</div>
    <table>
        <tr><td class="label">Wipe Method</td><td>{cert.get("wipe_method","")}</td></tr>
        <tr><td class="label">Hash Before</td><td>{cert.get("hash_before","")}</td></tr>
        <tr><td class="label">Hash After</td><td>{cert.get("hash_after","")}</td></tr>
        <tr><td class="label">Wipe Timestamp (UTC)</td><td>{cert.get("timestamp_utc","")}</td></tr>
        <tr><td class="label">Certificate Generated (UTC)</td><td>{cert.get("generated_at_utc","")}</td></tr>
    </table>

    <div class="section-title">Status</div>
    <p class="{ 'status-success' if cert.get('status') == 'SUCCESS' else 'status-warning' }">
        {cert.get("status")}
    </p>

    <p style="margin-top:40px;font-size:0.9em;color:#555;">
        This is an automatically generated certificate for demonstration and prototype purposes.
    </p>
</div>
</body>
</html>
"""


