#!/usr/bin/env python3
"""
📜 SOC CASEIRO - Log Viewer (estilo Hollywood)
Visualiza logs do Apache em tempo real
"""
import os
import re
import time
from datetime import datetime
from log_analyzer import LogAnalyzer

def cls():
    """Limpa a tela"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    """Header com arte ASCII"""
    header = """
    ╔════════════════════════════════════════════╗
    ║   📜 LOG VIEWER - VISUALIZADOR DE LOGS 📜   ║
    ║       Monitoramento de Tráfego em Tempo Real║
    ╚════════════════════════════════════════════╝
    """
    print("\033[1;32m" + header + "\033[0m")

def print_section(title, icon=""):
    """Título de seção"""
    print(f"\n\033[1;36m{'═' * 70}\033[0m")
    print(f"\033[1;36m{icon} {title}\033[0m")
    print(f"\033[1;36m{'═' * 70}\033[0m")

def color_by_status(status_code):
    """Retorna cor baseado no código HTTP"""
    try:
        status = int(status_code)
        if status < 300:
            return "\033[1;32m"  # Verde (sucesso)
        elif status < 400:
            return "\033[1;36m"  # Ciano (redirecionamento)
        elif status < 500:
            return "\033[1;33m"  # Amarelo (cliente erro)
        else:
            return "\033[1;31m"  # Vermelho (servidor erro)
    except:
        return "\033[0m"

def extract_status_code(log_line):
    """Extrai status code do log"""
    match = re.search(r' (\d{3}) ', log_line)
    return match.group(1) if match else "?"

def extract_ip(log_line):
    """Extrai IP do log"""
    match = re.match(r'^(\d+\.\d+\.\d+\.\d+)', log_line)
    return match.group(1) if match else "unknown"

def main():
    """Loop principal"""
    try:
        iteration = 0
        prev_lines = []
        
        while True:
            cls()
            print_header()
            
            # Coleta logs
            logs = LogAnalyzer.get_apache_logs(40)
            top_ips = LogAnalyzer.get_top_ips(5)
            
            # Destaca logs novos
            new_logs = [log for log in logs if log not in prev_lines]
            prev_lines = logs[:10]  # Guarda referência
            
            # ===== LOGS EM TEMPO REAL =====
            print_section("📊 ÚLTIMOS LOGS (TEMPO REAL)", "🔄")
            
            if logs:
                for idx, log in enumerate(logs[:25], 1):
                    # Extrai informações
                    ip = extract_ip(log)
                    status = extract_status_code(log)
                    color = color_by_status(status)
                    
                    # Marca logs novos
                    marker = "🆕" if log in new_logs else "📝"
                    
                    # Formata log (trunca para caber na tela)
                    log_clean = log.strip()[:65]
                    print(f"  {marker} {color}{status}\033[0m {ip:<15} {log_clean}")
            else:
                print("  \033[2;37m(nenhum log disponível)\033[0m")
            
            # ===== ESTATÍSTICAS =====
            print_section("📈 ESTATÍSTICAS DE ACESSO", "📊")
            print(f"\n  Total de logs disponíveis: \033[1;32m{len(logs)}\033[0m")
            print(f"  Logs novos nesta atualização: \033[1;33m{len(new_logs)}\033[0m")
            
            # ===== TOP IPs =====
            print_section("🔝 TOP 5 IPs", "👥")
            print(f"\n  {'Rank':<6} {'IP':<20} {'Requisições':<15}")
            print(f"  {'-' * 50}")
            
            for idx, (ip, count) in enumerate(top_ips.items(), 1):
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "  "
                print(f"  {medal} #{idx:<3} {ip:<20} {count}")
            
            # ===== ALERTAS =====
            print_section("⚠️  ALERTAS", "🚨")
            
            if new_logs:
                print(f"  \033[1;33m→ {len(new_logs)} novo(s) log(s) detectado(s)\033[0m")
            
            high_errors = sum(1 for log in logs if extract_status_code(log).startswith('5'))
            if high_errors > 0:
                print(f"  \033[1;31m→ {high_errors} erro(s) de servidor detectado(s)\033[0m")
            
            many_404s = sum(1 for log in logs if extract_status_code(log) == '404')
            if many_404s > 5:
                print(f"  \033[1;33m→ {many_404s} erro(s) 404 (Not Found) detectado(s)\033[0m")
            
            # ===== LEGENDA DE CORES =====
            print_section("🎨 LEGENDA", "📋")
            print(f"  \033[1;32m2xx\033[0m = Sucesso (Verde)")
            print(f"  \033[1;36m3xx\033[0m = Redirecionamento (Ciano)")
            print(f"  \033[1;33m4xx\033[0m = Erro Cliente (Amarelo)")
            print(f"  \033[1;31m5xx\033[0m = Erro Servidor (Vermelho)")
            
            # ===== RODAPÉ =====
            print(f"\n\033[2;37m{'═' * 70}\033[0m")
            print(f"\033[2;37m⏰ Atualizado: {datetime.now().strftime('%H:%M:%S')} | Atualização #{iteration}\033[0m")
            print(f"\033[2;37m💾 Pressione CTRL+C para sair\033[0m")
            
            iteration += 1
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Log Viewer encerrado.\033[0m")

if __name__ == "__main__":
    main()
