Red='\033[0;31m'
Green='\033[0;32m'
NC='\033[0m'
Yellow='\033[0;33m'

echo -e "\n ---> ${Green}Running runTraining.py${NC}\n\n"
python runTraining.py

echo -e "\n ---> ${Green}Running getCollections.py${NC}\n\n"
python getCollections.py

echo -e "\n ---> ${Green}Running generate_categories.py${NC}\n\n"
python generate_categories.py

echo -e "\n ---> ${Green}Running execute.py${NC}\n\n"
python execute.py

echo -e "\n ---> ${Green}Running convertAndStore.py${NC}\n\n"
python convertAndStore.py