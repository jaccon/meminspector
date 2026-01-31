#!/bin/bash
# MemInspector Swift - Quick Install Script
# Usage: curl -fsSL https://raw.githubusercontent.com/jaccon/meminspector/main/swift-version/install.sh | bash

set -e

echo "🔍 MemInspector Swift Native - Installation Script"
echo "=================================================="
echo ""

# Check for Swift compiler
if ! command -v swift &> /dev/null; then
    echo "❌ Swift compiler not found!"
    echo ""
    echo "Please install one of the following:"
    echo "  1. Xcode Command Line Tools: xcode-select --install"
    echo "  2. Full Xcode from App Store"
    echo ""
    exit 1
fi

echo "✓ Swift compiler found: $(swift --version | head -1)"
echo ""

# Create temporary directory
TMP_DIR=$(mktemp -d)
cd "$TMP_DIR"

echo "📥 Downloading source code..."
curl -sL https://github.com/jaccon/meminspector/archive/refs/tags/v2.0.1.tar.gz | tar xz
cd meminspector-2.0.1/swift-version

echo "🔨 Building MemInspector..."
swift build -c release

echo "📦 Installing to /usr/local/bin..."
sudo cp .build/release/MemInspector /usr/local/bin/meminspector
sudo chmod +x /usr/local/bin/meminspector

echo "🧹 Cleaning up..."
cd /
rm -rf "$TMP_DIR"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📊 Usage:"
echo "  meminspector --tui       # Colored terminal interface"
echo "  meminspector --refresh   # Continuous refresh mode"
echo "  meminspector --graph     # ASCII graphs"
echo "  meminspector --help      # Show all options"
echo ""
echo "🎉 Enjoy MemInspector! Developed by Jaccon"
