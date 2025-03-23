echo "Endload Setup"

# Install Python and dependencies
sudo apt install python3.12 python3.12-venv python3.12-pip

# Create a virtual environment
python3.12 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python modules
pip install bcrypt pyfiglet termcolor requests flask python-dotenv

echo "Installed Python Modules"

# Run setup.py (if applicable)
python setup.py
