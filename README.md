# HSE_ML_P2024
HSE second course final project about teaching AI to play parking game.

# Development setup

Create env:
```shell
python -m venv ultimate_parking

.\ultimate_parking\Scripts\activate

pip install -r requirements.txt
```

Save install:
```shell
pip freeze > requirements.txt
```

Build debug
```shell
python ./main.py
```

Check build release:
```shell
mypy .

pyinstaller.exe ./main.py

.\build\main\main.exe
```
