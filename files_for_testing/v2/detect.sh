if [ "$1" = "" ]; then
    echo "Отсутствует источник для детекции"
    exit 1
fi
python detect.py --weights cars_best_v2.pt --source $1
