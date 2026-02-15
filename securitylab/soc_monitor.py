#!/usr/bin/env python3
"""
🔥 SOC CASEIRO - Monitor Principal (estilo Hollywood)
Corre em tempo real com arte ASCII
"""
import os
import time
from datetime import datetime
from log_analyzer import LogAnalyzer

def cls():
    """Limpa a tela"""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_bar(value, max_val=100, length=30):
    """Cria uma barra de progresso"""
    fill = int((value / max_val) * length)
    bar = '█' * fill + '░' * (length - fill)
    return f"[{bar}] {value:.1f}%"

def print_header():
    """Imprime header com arte ASCII"""
    header = """
    ╔══════════════════════════════════════════╗
    ║   🔥 SOC CASEIRO - MONITOR PRINCIPAL 🔥   ║
    ║     Sistema de Monitoramento em Tempo Real║
    ╚══════════════════════════════════════════╝
    """
    print("\033[1;31m" + header + "\033[0m")

def print_section(title):
    """Imprime título de seção"""
    print(f"\n\033[1;36m{'═' * 50}\033[0m")
    print(f"\033[1;36m▶ {title}\033[0m")
    print(f"\033[1;36m{'═' * 50}\033[0m")

def print_metric(name, value, unit="", icon=""):
    """Imprime uma métrica formatada"""
    print(f"  {icon} {name:<25} \033[1;32m{value}{unit}\033[0m")

def print_status(label, value, threshold=None):
    """Imprime status com cores"""
    if threshold and isinstance(value, (int, float)):
        if value > threshold:
            color = "\033[1;31m"  # Vermelho
            marker = "🔴"
        elif value > threshold * 0.7:
            color = "\033[1;33m"  # Amarelo
            marker = "🟡"
        else:
            color = "\033[1;32m"  # Verde
            marker = "🟢"
        print(f"  {marker} {label:<25} {color}{value:.1f}%\033[0m")
    else:
        print(f"  • {label:<25} {value}")

def main():
    """Loop principal"""
    try:
        while True:
            cls()
            print_header()
            
            # Coleta dados
            metrics = LogAnalyzer.get_system_metrics()
            connections = LogAnalyzer.get_network_connections()
            ddos_info = LogAnalyzer.detect_ddos()
            
            # ===== SISTEMA =====
            print_section("⚙️  SISTEMA")
            uptime_h = metrics['uptime_seconds'] // 3600
            uptime_m = (metrics['uptime_seconds'] % 3600) // 60
            print_metric("Uptime", f"{uptime_h}h {uptime_m}m", icon="⏱️")
            print_metric("CPUs", f"{metrics['cpu_count']} cores", icon="⚡")
            
            # ===== RECURSOS =====
            print_section("📊 RECURSOS")
            print(f"\n  CPU:\n{get_bar(metrics['cpu_percent'])}")
            print(f"\n  RAM: {metrics['ram_used_gb']}GB / {metrics['ram_total_gb']}GB\n{get_bar(metrics['ram_used_percent'])}")
            print(f"\n  DISCO:\n{get_bar(metrics['disk_percent'])}")
            
            print_status("CPU Uso", metrics['cpu_percent'], 80)
            print_status("RAM Uso", metrics['ram_used_percent'], 80)
            print_status("DISCO Uso", metrics['disk_percent'], 90)
            
            # ===== REDE =====
            print_section("🌐 REDE")
            print_metric("Conexões Totais", connections.get('total_connections', 0), icon="🔌")
            print_metric("Porta 80 (HTTP)", connections.get('port_80_connections', 0), icon="🌍")
            print_metric("Porta 443 (HTTPS)", connections.get('port_443_connections', 0), icon="🔒")
            print_metric("Estabelecidas", connections.get('established_connections', 0), icon="📡")
            
            # ===== SEGURANÇA =====
            print_section("🚨 SEGURANÇA & DDoS")
            
            risk = ddos_info.get('risk_level', 'unknown')
            risk_icons = {
                'critical': '🔴 CRÍTICO',
                'high': '🟠 ALTO',
                'low': '🟢 BAIXO',
                'unknown': '❓ DESCONHECIDO'
            }
            print_metric("Nível de Risco", risk_icons.get(risk, risk), icon="⚠️")
            
            print_metric("IPs Únicos", ddos_info.get('total_unique_ips', 0), icon="🧑‍💻")
            print_metric("IPs Suspeitos", len(ddos_info.get('suspicious_ips', {})), icon="🚫")
            
            if ddos_info.get('suspicious_ips'):
                print("\n  \033[1;31m⛔ IPs SUSPEITOS:\033[0m")
                for ip, count in list(ddos_info['suspicious_ips'].items())[:3]:
                    print(f"     {ip:<15} → \033[1;31m{count} requisições\033[0m")
            
            top_ips = ddos_info.get('top_ips', {})
            if top_ips:
                print("\n  📈 TOP 5 IPs:")
                for i, (ip, count) in enumerate(list(top_ips.items())[:5], 1):
                    print(f"     {i}. {ip:<15} → {count} requisições")
            
            # ===== RODAPÉ =====
            print(f"\n\033[2;37m{'═' * 50}\033[0m")
            print(f"\033[2;37m⏰ Atualizado: {datetime.now().strftime('%H:%M:%S')}\033[0m")
            print(f"\033[2;37m💾 Pressure CTRL+C para sair\033[0m")
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Monitor encerrado.\033[0m")

if __name__ == "__main__":
    main()
