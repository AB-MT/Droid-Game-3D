# welcome
GREEN='\033[0;32m' # green color
NC='\033[0m' # No Color
printf "Welcome to ${GREEN} Droid Game 3D ${NC} \n"

# Installing Python modules
echo Installing Python modules..
pip install -r requriements.txt

# Building with Nuitka
echo Compilation...
python3 -m nuitka game.py

echo Done!
