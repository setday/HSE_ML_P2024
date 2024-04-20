# Ultimate Parking
HSE second course final project about teaching AI to play parking game.

![GitHub](https://img.shields.io/github/license/setday/HSE_ML_P2024)
![GitHub last commit](https://img.shields.io/github/last-commit/setday/HSE_ML_P2024)
![GitHub top language](https://img.shields.io/github/languages/top/setday/HSE_ML_P2024)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/setday/HSE_ML_P2024)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/setday/HSE_ML_P2024)

![Game screenshot](./data/screenshots/1709931940.2689118.png)

## Description

The game is a 2D parking simulator. The player has to park a car in a parking spot. The car is controlled by the player using the WASD keys + space for hand brake. The car has to be parked in a parking spot without hitting any obstacles. The game is over when the car hits an obstacle or the parking spot. The game is won when the car is parked in the parking spot.

Special features:
- The car has a limited amount of fuel. The fuel is consumed when the car is moving. The fuel can be refilled by picking up fuel canisters.
- The car has a limited amount of health. The health is reduced when the car hits an obstacle. The health can be refilled by picking up health canisters.
- The car has a limited amount of time to park. The time is reduced when the car is moving. The time can be refilled by picking up time canisters.

Special keys:
- r - super-slowdown
- f6 - screenshot
- f7 - reset health

## Installation
    
```shell
pip install -r requirements.txt

python ./main.py
```

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

## Team
- [Alexander Serkov](https://github.com/setday/)
- [Vladimir Zakharov](https://github.com/yv0vaa/)
- [Artem Batygin](https://github.com/Tematikys/)
