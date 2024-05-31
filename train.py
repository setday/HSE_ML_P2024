from src.game_engine.controllers.TrainAIController import TrainAIController

if __name__ == "__main__":
    train = TrainAIController(view_mode=False, spectate_mode=False)
    train.run()
