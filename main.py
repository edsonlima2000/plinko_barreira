import pygame

from game.game import PlinkoGame


def main() -> None:
    pygame.init()
    game = PlinkoGame()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
