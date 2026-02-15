#!/bin/bash

# 🔥 SOC CASEIRO - Master Launcher
# Roda todos os 3 monitors em paralelo (estilo Hollywood)

PYTHON="/home/marcosgomes/siteweb/venv/bin/python3"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   🔥 SOC CASEIRO - HOLLYWOOD MODE ATIVADO 🔥           ║"
echo "║   Iniciando 3 shells independentes de monitoramento... ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "💡 Dica: Abra 3 terminais diferentes para melhor visualização!"
echo ""
echo "Opções:"
echo "  1) Monitor Principal (soc_monitor.py)"
echo "  2) Detector DDoS (ddos_detector.py)"
echo "  3) Log Viewer (logs_viewer.py)"
echo "  4) Tudo junto (em subshells)"
echo ""
read -p "Escolha uma opção [1-4]: " option

case $option in
    1)
        echo "[1] Iniciando Monitor Principal..."
        $PYTHON "$DIR/soc_monitor.py"
        ;;
    2)
        echo "[2] Iniciando Detector DDoS..."
        $PYTHON "$DIR/ddos_detector.py"
        ;;
    3)
        echo "[3] Iniciando Log Viewer..."
        $PYTHON "$DIR/logs_viewer.py"
        ;;
    4)
        echo "[*] Iniciando todos os 3 monitors em paralelo..."
        echo ""
        echo "⚠️  ATENÇÃO: Abra 3 janelas de terminal diferentes!"
        echo "   Shell 1: " && sleep 1
        gnome-terminal --title="SOC - Monitor Principal" -- bash -c "$PYTHON $DIR/soc_monitor.py; bash" 2>/dev/null || \
        xterm -title "SOC - Monitor Principal" -e "$PYTHON $DIR/soc_monitor.py" 2>/dev/null || \
        konsole --title "SOC - Monitor Principal" -e "$PYTHON $DIR/soc_monitor.py" 2>/dev/null || \
        echo "Terminal não encontrado. Execute manualmente: $PYTHON $DIR/soc_monitor.py"
        
        sleep 1
        echo ""
        echo "   Shell 2: " && sleep 1
        gnome-terminal --title="SOC - Detector DDoS" -- bash -c "$PYTHON $DIR/ddos_detector.py; bash" 2>/dev/null || \
        xterm -title "SOC - Detector DDoS" -e "$PYTHON $DIR/ddos_detector.py" 2>/dev/null || \
        konsole --title "SOC - Detector DDoS" -e "$PYTHON $DIR/ddos_detector.py" 2>/dev/null || \
        echo "Terminal não encontrado. Execute manualmente: $PYTHON $DIR/ddos_detector.py"
        
        sleep 1
        echo ""
        echo "   Shell 3: " && sleep 1
        gnome-terminal --title="SOC - Log Viewer" -- bash -c "$PYTHON $DIR/logs_viewer.py; bash" 2>/dev/null || \
        xterm -title "SOC - Log Viewer" -e "$PYTHON $DIR/logs_viewer.py" 2>/dev/null || \
        konsole --title "SOC - Log Viewer" -e "$PYTHON $DIR/logs_viewer.py" 2>/dev/null || \
        echo "Terminal não encontrado. Execute manualmente: $PYTHON $DIR/logs_viewer.py"
        
        echo ""
        echo "✅ Todos os monitors foram iniciados!"
        echo "💾 Pressione CTRL+C em cada janela para encerrar"
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac
