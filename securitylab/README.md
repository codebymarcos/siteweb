# 🔥 SOC CASEIRO - Sistema de Monitoramento de Segurança

**Estilo Hollywood com Múltiplos Shells em Tempo Real**

---

## 📋 Descrição

Um sistema de monitoramento de segurança local (SOC - Security Operations Center) que roda no terminal, com visualização tipo "hackerland" em arte ASCII. Monitora em tempo real:

- ⚡ CPU, RAM, DISCO
- 🌐 Conexões de rede
- 🚨 Detecção de DDoS
- 📜 Logs do Apache
- 👥 IPs suspeitos
- 📊 Status HTTP

---

## 🚀 Instalação

### Pré-requisitos

```bash
# Instalar dependências do sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip apache2

# Ou para Kali/Arch
sudo pacman -S python apache
```

### Setup do Projeto

```bash
cd /home/marcosgomes/siteweb/securitylab

# Instalar dependências Python
pip install -r requirements.txt
```

---

## 🎯 Como Usar

### Opção 1: Monitor Principal (Métricas do Sistema)

```bash
python3 soc_monitor.py
```

Mostra:
- CPU, RAM, DISCO em tempo real
- Uptime do sistema
- Conexões abertas
- Detecção de DDoS

### Opção 2: Detector de DDoS

```bash
python3 ddos_detector.py
```

Mostra:
- Nível de risco (crítico/alto/baixo)
- IPs suspeitos
- Top 10 IPs mais ativos
- Análise de tráfego

### Opção 3: Log Viewer

```bash
python3 logs_viewer.py
```

Mostra:
- Últimos logs do Apache em tempo real
- Códigos HTTP coloridos (2xx/3xx/4xx/5xx)
- Estatísticas de acesso
- Alertas de erros

### Opção 4: Modo Hollywood (3 Monitors em Paralelo)

```bash
bash soc_launcher.sh
```

Selecione opção **4** para abrir os 3 monitors em shells diferentes (como no filme The Matrix! 🎬).

---

## 📊 Estrutura

```
securitylab/
├── soc_monitor.py      # Monitor principal
├── ddos_detector.py    # Detector de DDoS
├── logs_viewer.py      # Visualizador de logs
├── soc_launcher.sh     # Script para rodar tudo
├── log_analyzer.py     # Biblioteca de análise
├── requirements.txt    # Dependências
└── README.md          # Este arquivo
```

---

## 🎨 Cores e Símbolos

| Cor | Significado |
|-----|------------|
| 🟢 Verde | OK / Seguro |
| 🟡 Amarelo | Aviso / Monitorar |
| 🔴 Vermelho | Crítico / Suspeito |
| 🔵 Ciano | Informação |

---

## 🔍 Exemplos de Saída

### Monitor Principal
```
╔══════════════════════════════════════════╗
║   🔥 SOC CASEIRO - MONITOR PRINCIPAL 🔥   ║
╚══════════════════════════════════════════╝

⚙️  SISTEMA
═════════════════════════════════════════════════
  ⏱️  Uptime                  4h 23m
  ⚡ CPUs                     8 cores

📊 RECURSOS
═════════════════════════════════════════════════
  CPU:
  [████████████░░░░░░░░░░░░░░░] 45.2%
  
  🟢 CPU Uso       45.2%
  🟢 RAM Uso       62.1%
  🟡 DISCO Uso     88.5%
```

### DDoS Detector
```
╔═══════════════════════════════════════════╗
║   🚨 DETECTOR DE DDoS - MONITORAMENTO 🚨   ║
╚═══════════════════════════════════════════╝

  ╔════════════════════════════════════════════╗
  ║ NÍVEL DE AMEAÇA: 🔴 CRÍTICO              ║
  ║ ████████████████████                      ║
  ╚════════════════════════════════════════════╝

🚫 IPs SUSPEITOS DETECTADOS
═════════════════════════════════════════════════
  192.168.1.100        245 requisições  CRÍTICO
  10.0.0.50            156 requisições  ALTO
  172.16.0.20          87  requisições  MÉDIO
```

### Log Viewer
```
📜 ÚLTIMOS LOGS (TEMPO REAL)
═════════════════════════════════════════════════
  🆕 200 192.168.1.1      GET /index.html HTTP/1.1
  📝 404 10.0.0.50        GET /admin.php HTTP/1.1
  🆕 500 172.16.0.20      POST /api/users HTTP/1.1
  📝 200 192.168.1.5      GET /static/style.css HTTP/1.1
```

---

## ⚙️ Configuração

### Limiar de DDoS

Edite [log_analyzer.py](log_analyzer.py):

```python
DDOS_THRESHOLD = 50  # Requisições por IP em curto período
```

### Caminho do Log

```python
LOG_PATH = "/var/log/apache2/access.log"
```

Altere se seus logs estão em outro local.

---

## 🔧 Troubleshooting

### "Log file not found"

```bash
# Verifique se Apache está rodando
sudo systemctl status apache2

# Se não estiver, inicie
sudo systemctl start apache2

# Verifique o caminho exato do log
ls -la /var/log/apache2/access.log
```

### "Permission denied"

```bash
# Para ver conexões de rede, pode precisar de sudo
sudo python3 soc_monitor.py
```

### "ModuleNotFoundError: No module named 'psutil'"

```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt
```

---

## 📈 Dicas de Uso

1. **Monitoramento 24/7**: Deixe os scripts rodando em screens/tmux
   ```bash
   screen -S soc-monitor python3 soc_monitor.py
   ```

2. **Logs persistentes**: Redirecione para arquivo
   ```bash
   python3 logs_viewer.py > logs_viewer_$(date +%s).log &
   ```

3. **Alertas automáticos**: Integre com ferramentas como:
   - `ntfy` para notificações
   - `webhook` para Slack/Discord
   - Systemd timers para ações agendadas

---

## 📦 Dependências

- **Python 3.8+**
- **psutil** - Métricas de sistema
- **Apache2** - Servidor web (para logs)

---

## 🎓 Aprendizado

Este projeto demonstra:
- ✅ Processamento de logs em Python
- ✅ Monitoramento de sistema com psutil
- ✅ Interface de terminal com ANSI colors e arte ASCII
- ✅ Detecção de anomalias (padrão de ataque)
- ✅ Análise de tráfego de rede
- ✅ Scripting shell para automação
- ✅ Boas práticas de segurança

---

## 📝 Licença

Livre para uso pessoal e educacional.

---

## 📞 Suporte

Para dúvidas e melhorias, consulte a documentação ou execute:

```bash
python3 -h  # Ajuda geral
```

---

**Made with 🔥 by SOC Caseiro** | 2026
