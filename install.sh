#!/bin/bash
echo "╔══════════════════════════════════════════════════╗"
echo "║   NETGITS Quiz - Installation                    ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "📦 Installing NETGITS Quiz..."
sudo dpkg -i netgits-quiz_1.0.0-beta_amd64.deb
sudo apt install -f -y
echo ""
echo "✅ Installation complete!"
echo "🚀 Run: netgits-quiz"
echo "🗑️  Uninstall: sudo dpkg -r netgits-quiz"
