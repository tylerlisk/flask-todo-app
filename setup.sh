# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies (if needed)
sudo apt-get install -y python3-pip python3-dev python3-venv build-essential

# Create a directory for your app (if not already created)
mkdir -p /flask_todo_app
cd /flask_todo_app

# Set up the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Start the Flask app (for development)
flask run --host=0.0.0.0


