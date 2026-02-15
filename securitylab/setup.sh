#!/bin/bash
# 🔥 SOC CASEIRO - Setup de Dependências
# Execute este script para configurar o ambiente

set -e

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   🔧 SOC CASEIRO - INSTALADOR DE DEPENDÊNCIAS 🔧       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$DIR/venv"

# Detecta Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ Python não encontrado! Instale com:"
    echo "   sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

echo "✓ Python encontrado: $($PYTHON --version)"

# Cria venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "📦 Criando ambiente virtual..."
    $PYTHON -m venv "$VENV_DIR"
    echo "✓ Venv criado em: $VENV_DIR"
else
    echo "✓ Venv já existe em: $VENV_DIR"
fi

# Ativa venv
echo ""
echo "🔄 Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

# Atualiza pip
echo ""
echo "📥 Atualizando pip..."
pip install --upgrade pip -q

# Instala dependências
echo ""
echo "📥 Instalando dependências..."
pip install -r "$DIR/requirements.txt" -q

# Verifica instalação
echo ""
echo "🔍 Verificando instalação..."
$PYTHON -c "import psutil; print(f'✓ psutil {psutil.__version__}')"

# Torna scripts executáveis
echo ""
echo "🔒 Configurando permissões..."
chmod +x "$DIR/soc_monitor.py" 2>/dev/null || true
chmod +x "$DIR/ddos_detector.py" 2>/dev/null || true
chmod +x "$DIR/logs_viewer.py" 2>/dev/null || true
chmod +x "$DIR/soc_launcher.sh" 2>/dev/null || true
echo "✓ Permissõesconfiguradasas"

# Finaliza
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Como usar:"
echo ""
echo "   # Ative o ambiente virtual primeiro:"
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "   # Depois execute um dos monitores:"
echo "   python3 soc_monitor.py       # Monitor principal"
echo "   python3 ddos_detector.py     # Detector de DDoS"
echo "   python3 logs_viewer.py       # Visualizador de logs"
echo ""
echo "   # Ou use o launcher:"
echo "   bash soc_launcher.sh"
echo ""
echo "💡 Dica: Para desativar o venv, digite: deactivate"
echo ""
