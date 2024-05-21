from src.game_engine.controllers.TrainAI import Train


if __name__ == "__main__":
    train = Train(view_mode=False, spectate_mode=False)
    train.run()
