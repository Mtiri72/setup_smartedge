#!/bin/bash

set -e

NIKSS_DIR="$HOME/nikss"

# Install dependencies
sudo apt update
sudo apt install -y \
  make cmake gcc git libgmp-dev libelf-dev zlib1g-dev libjansson-dev

# Clone the nikss repository with submodules
echo "📥 Cloning NIKSS repository..."
git clone --recursive https://github.com/NIKSS-vSwitch/nikss.git "$NIKSS_DIR"
cd "$NIKSS_DIR"

# Build libbpf
./build_libbpf.sh

# Create build directory
mkdir -p build
cd build

# Run cmake and build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j"$(nproc)"
sudo make install

# Ensure linker can find the shared libraries
if [ -d "/usr/local/lib" ]; then
  echo "/usr/local/lib" | sudo tee /etc/ld.so.conf.d/nikss.conf > /dev/null
  sudo ldconfig
fi

echo "✅ NIKSS installation completed successfully."
echo "🔧 You can now use 'nikss-ctl' to manage P4 pipelines."
