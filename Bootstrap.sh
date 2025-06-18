#!/bin/bash

REPO_URL="https://github.com/zoxerus/smartedge.git"
PROGRAM_DIR="$HOME/smartedge_program"

# Function: install base tools (git, pip, venv, curl)
install_base_tools() {
    echo "🔧 Updating apt sources and enabling universe repo..."
    sudo add-apt-repository universe -y
    sudo apt-get update

    echo "📦 Installing missing base tools: git, pip, venv..."
    sudo apt-get install -y git python3-pip python3-venv curl

    if ! command -v git &>/dev/null; then
        echo "❌ Git is not available and could not be installed. Please check your apt sources."
        exit 1
    fi
}


# Step 1: Check internet connection
check_internet() {
    echo "🔌 Checking internet connectivity..."
    if ping -q -c 1 -W 2 8.8.8.8 > /dev/null; then
        echo "✅ Internet connection: OK"
    else
        echo "❌ No internet connection. Please connect and retry."
        exit 1
    fi
}

# Step 2: Ensure Python 3.10+ and tools
ensure_python() {
    echo "🐍 Checking Python installation..."
    if command -v python3 &>/dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if [[ $(echo "$PYTHON_VERSION >= 3.10" | bc) -eq 1 ]]; then
            echo "✅ Python $PYTHON_VERSION is installed."
        else
            echo "⏬ Upgrading to Python 3.10..."
            sudo apt update && sudo apt install -y python3.10 python3.10-venv python3.10-distutils
            sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
        fi
    else
        echo "⏬ Installing Python 3.10..."
        sudo apt update && sudo apt install -y python3.10 python3.10-venv python3.10-distutils
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
    fi

    sudo apt install -y python3-pip python3-venv
}

# Step 3: Clone the SmartEdge repo
clone_program_repo() {
    echo "📥 Cloning SmartEdge repository..."
    if [ -d "$PROGRAM_DIR/.git" ]; then
        echo "🔄 Updating existing SmartEdge repo..."
        git -C "$PROGRAM_DIR" pull
    elif [ -d "$PROGRAM_DIR" ]; then
        echo "⚠️  Folder $PROGRAM_DIR exists but is not a git repo. Please delete or move it."
        exit 1
    else
        git clone "$REPO_URL" "$PROGRAM_DIR"
    fi
}

# Step 4: Run the Python installer (handles everything else)
launch_python_installer() {
    echo "🚀 Launching the SmartEdge Python installer..."
    cd "$HOME/setup_smartedge" || exit 1
    python3 smartedge-installer.py
}

# Run all steps
check_internet
install_base_tools
ensure_python
clone_program_repo
launch_python_installer

echo "✅ Bootstrap complete — handover to Python installer done!"
