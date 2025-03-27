echo "Endload Setup"

echo "Downloading From github"

sudo curl -i "https://github.com/EndlessSB/endload/archive/refs/heads/main.zip" > /endload

"Sucsess"

cd /endload

# Install Python and dependencies
sudo apt install python3.12 python3.12-venv 

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python modules
pip install bcrypt pyfiglet termcolor requests flask python-dotenv

echo "Installed Python Modules"

# Run setup.py (if applicable)
python setup.py
