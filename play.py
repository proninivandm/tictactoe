import Game
import argparse
parser = argparse.ArgumentParser(description='play tictactoe')
parser.add_argument('-n', dest='n', type=int, help='desk size')
parser.add_argument('-k', dest='k', type=int, help='win length')
parser.add_argument('--mode', dest='mode', type=str, help='playing mode')
game=Game.TicTacToe(parser.parse_args().n,parser.parse_args().k,parser.parse_args().mode)
game.play()