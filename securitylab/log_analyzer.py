import os
import psutil
import re
import subprocess
import socket
from collections import Counter
from datetime import datetime

class LogAnalyzer:
    LOG_PATH = "/var/log/apache2/access.log"
    DDOS_THRESHOLD = 50
    
    # IPs que devem ser ignorados (localhost, própria máquina)
    WHITELIST = {'127.0.0.1', 'localhost', '::1'}
    
    @staticmethod
    def get_local_ips():
        """Retorna todos os IPs da máquina local"""
        local_ips = set(LogAnalyzer.WHITELIST)
        try:
            for iface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        local_ips.add(addr.address)
        except:
            pass
        return local_ips
    
    @staticmethod
    def is_local_ip(ip):
        """Verifica se o IP é local"""
        local_ips = LogAnalyzer.get_local_ips()
        return ip in local_ips
    
    @staticmethod
    def get_system_metrics():
        """Coleta métricas de CPU, RAM, disco"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "cpu_count": psutil.cpu_count(),
            "ram_used_percent": psutil.virtual_memory().percent,
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "disk_percent": psutil.disk_usage("/").percent,
            "uptime_seconds": int(datetime.now().timestamp() - psutil.boot_time())
        }
    
    @staticmethod
    def get_network_connections():
        """Conta conexões abertas"""
        try:
            connections = psutil.net_connections(kind='inet')
            port_80 = [c for c in connections if c.laddr.port == 80]
            port_443 = [c for c in connections if c.laddr.port == 443]
            
            return {
                "total_connections": len(connections),
                "port_80_connections": len(port_80),
                "port_443_connections": len(port_443),
                "established_connections": len([c for c in connections if c.status == 'ESTABLISHED'])
            }
        except:
            return {"total_connections": 0}
    
    @staticmethod
    def detect_ddos():
        """Detecta possível DDoS"""
        try:
            with open(LogAnalyzer.LOG_PATH, "r") as f:
                lines = f.readlines()
            
            if not lines:
                return {"suspicious_ips": {}, "risk_level": "low", "local_ips_filtered": 0}
            
            recent_logs = lines[-1000:]
            ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'
            ips = []
            local_ips = LogAnalyzer.get_local_ips()
            local_filtered = 0
            
            for log in recent_logs:
                match = re.match(ip_pattern, log)
                if match:
                    ip = match.group(1)
                    if ip in local_ips:
                        local_filtered += 1
                    else:
                        ips.append(ip)
            
            ip_counts = Counter(ips)
            suspicious_ips = {ip: count for ip, count in ip_counts.items() 
                            if count > LogAnalyzer.DDOS_THRESHOLD}
            
            risk_level = "critical" if len(suspicious_ips) > 5 else "high" if suspicious_ips else "low"
            
            return {
                "suspicious_ips": suspicious_ips,
                "risk_level": risk_level,
                "total_unique_ips": len(ip_counts),
                "top_ips": dict(ip_counts.most_common(5)),
                "local_filtered": local_filtered
            }
        except:
            return {"error": "N/A", "risk_level": "unknown"}
    
    @staticmethod
    def get_apache_logs(lines_count=20):
        """Retorna últimas linhas do log"""
        try:
            with open(LogAnalyzer.LOG_PATH, "r") as f:
                all_lines = f.readlines()
            return all_lines[-lines_count:][::-1]
        except:
            return []
    
    @staticmethod
    def get_top_ips(limit=5):
        """Top IPs mais frequentes (exclui IPs locais)"""
        try:
            with open(LogAnalyzer.LOG_PATH, "r") as f:
                lines = f.readlines()
            
            ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'
            local_ips = LogAnalyzer.get_local_ips()
            ips = []
            for log in lines:
                match = re.match(ip_pattern, log)
                if match:
                    ip = match.group(1)
                    if ip not in local_ips:
                        ips.append(ip)
            
            ip_counts = Counter(ips)
            return dict(ip_counts.most_common(limit))
        except:
            return {}

