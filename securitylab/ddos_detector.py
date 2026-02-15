#!/usr/bin/env python3
"""
🚨 SOC CASEIRO - DDoS Detector (estilo Hollywood)
Monitora atividades suspeitas em tempo real
"""
import os
import time
from datetime import datetime
from log_analyzer import LogAnalyzer

def cls():
    """Limpa a tela"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    """Header com arte ASCII"""
    header = """
    ╔═══════════════════════════════════════════╗
    ║   🚨 DETECTOR DE DDoS - MONITORAMENTO 🚨   ║
    ║        Detecção em Tempo Real              ║
    ╚═══════════════════════════════════════════╝
    """
    print("\033[1;33m" + header + "\033[0m")

def print_threat_level(level):
    """Mostra nível de ameaça com animação"""
    levels = {
        'critical': ('🔴 CRÍTICO', '\033[1;31m'),
        'high': ('🟠 ALTO', '\033[1;33m'),
        'low': ('🟢 BAIXO', '\033[1;32m'),
        'unknown': ('❓ DESCONHECIDO', '\033[0;37m')
    }
    
    text, color = levels.get(level, ('?', '\033[0m'))
    
    bars = '█' * 20
    print(f"\n  {color}╔{'═' * 48}╗\033[0m")
    print(f"  {color}║ NÍVEL DE AMEAÇA: {text:<25} ║\033[0m")
    print(f"  {color}║ {bars:<46} ║\033[0m")
    print(f"  {color}╚{'═' * 48}╝\033[0m")

def print_section(title, icon=""):
    """Título de seção"""
    print(f"\n\033[1;36m{'═' * 55}\033[0m")
    print(f"\033[1;36m{icon} {title}\033[0m")
    print(f"\033[1;36m{'═' * 55}\033[0m")

def animate_scanning():
    """Animação de scan"""
    states = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    for state in states:
        print(f"\r\033[1;33m{state} Analisando tráfego...\033[0m", end='', flush=True)
        time.sleep(0.03)
    print()

def main():
    """Loop principal"""
    try:
        iteration = 0
        while True:
            cls()
            print_header()
            
            animate_scanning()
            
            # Coleta dados
            ddos_info = LogAnalyzer.detect_ddos()
            top_ips = LogAnalyzer.get_top_ips(10)
            
            risk_level = ddos_info.get('risk_level', 'unknown')
            
            # Mostra nível de ameaça
            print_threat_level(risk_level)
            
            # ===== ESTATÍSTICAS =====
            print_section("📊 ESTATÍSTICAS", "📈")
            print(f"  Total de IPs únicos      \033[1;32m{ddos_info.get('total_unique_ips', 0)}\033[0m")
            print(f"  IPs suspeitos detectados \033[1;31m{len(ddos_info.get('suspicious_ips', {}))}\033[0m")
            
            # ===== IPs SUSPEITOS =====
            suspicious = ddos_info.get('suspicious_ips', {})
            if suspicious:
                print_section("🚫 IPs SUSPEITOS DETECTADOS", "⛔")
                print(f"\n  \033[1;31m{'IP':<20} {'REQUISIÇÕES':<20} STATUS\033[0m")
                print(f"  \033[1;31m{'-' * 50}\033[0m")
                
                for ip, count in sorted(suspicious.items(), key=lambda x: x[1], reverse=True):
                    severity = "CRÍTICO" if count > 200 else "ALTO" if count > 100 else "MÉDIO"
                    color = "\033[1;31m" if count > 200 else "\033[1;33m"
                    print(f"  {ip:<20} {color}{count:<20} {severity}\033[0m")
            else:
                print_section("✅ NENHUM IP SUSPEITO DETECTADO", "🟢")
            
            # ===== TOP IPs =====
            print_section("📡 TOP 10 IPs MAIS ATIVOS", "🔝")
            print(f"\n  {'#':<3} {'IP':<20} {'REQUISIÇÕES':<15} RISCO")
            print(f"  {'-' * 50}")
            
            for idx, (ip, count) in enumerate(sorted(top_ips.items(), key=lambda x: x[1], reverse=True), 1):
                # Detecta se é suspeito
                is_suspicious = ip in suspicious
                if is_suspicious:
                    icon = "🚫"
                    color = "\033[1;31m"
                    risk = "SUSPEITO"
                elif count > 50:
                    icon = "⚠️"
                    color = "\033[1;33m"
                    risk = "MONITORAR"
                else:
                    icon = "✓"
                    color = "\033[1;32m"
                    risk = "OK"
                
                print(f"  {idx:<3} {ip:<20} {color}{count:<15}{risk}\033[0m {icon}")
            
            # ===== ANÁLISE =====
            print_section("🔍 ANÁLISE", "🔎")
            
            if risk_level == 'critical':
                print("  \033[1;31m[!] ALERTA CRÍTICO!\033[0m")
                print("      - Múltiplos IPs com comportamento suspeito")
                print("      - Possível ataque coordenado detectado")
                print("      - Ação recomendada: Investigar imediatamente")
            elif risk_level == 'high':
                print("  \033[1;33m[!] ALERTA DE RISCO ALTO\033[0m")
                print(f"      - {len(suspicious)} IPs com padrão de ataque")
                print("      - Ação recomendada: Monitorar de perto")
            else:
                print("  \033[1;32m[✓] Sistema seguro\033[0m")
                print("      - Nenhuma atividade suspeita detectada")
                print("      - Tráfego normal")
            
            # ===== RODAPÉ =====
            print(f"\n\033[2;37m{'═' * 55}\033[0m")
            print(f"\033[2;37m⏰ Atualizado: {datetime.now().strftime('%H:%M:%S')} | Scan #{iteration}\033[0m")
            print(f"\033[2;37m💾 Pressione CTRL+C para sair\033[0m")
            
            iteration += 1
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Detector encerrado.\033[0m")

if __name__ == "__main__":
    main()
