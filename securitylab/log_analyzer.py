def analyze_logs():
    with open("/var/log/apache2/access.log", "r") as f:
        return {"total_requests": len(f.readlines())}

