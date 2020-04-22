# !/usr/bin/Anaconda3/python
# -*- coding: utf-8 -*-
from func_timeout import func_timeout, FunctionTimedOut
import datetime
from board import Board
from copy import deepcopy
import random

class Random_Game(object):
    def __init__(self,new_board,color):
        self.board = Board()
        for i in range(8):
            for j in range(8):
                self.board._board[i][j] = new_board[i][j]        
        # 定义棋盘上当前下棋棋手，先默认是 None
        self.current_player = color

    # 切换当前棋手
    def switch_player(self,color):
        if color=='X':
            return 'O'
        else:
            return 'X'

    def run(self):
        # 初始化胜负结果和棋子差
        winner = None
        diff = -1

        while True:
            # 获取当前下棋方合法落子位置
            legal_actions = list(self.board.get_legal_actions(self.current_player))
            # 判断是否需要跳步或结束游戏
            if len(legal_actions) == 0:
                # 判断游戏是否结束
                if self.game_over():
                    # 游戏结束，双方都没有合法位置
                    winner, diff = self.board.get_winner()  # 得到赢家 0,1,2
                    break
                else:
                    self.current_player = self.switch_player(self.current_player)
                    # 另一方有合法位置,切换下棋方
                    continue
            
            # 当前下棋方随机下一步棋
            action = random.choice(legal_actions)
            # 更新棋局
            self.board._move(action, self.current_player)
            #print("Assuming:")
            #self.board.display()
            # 判断游戏是否结束
            if self.game_over():
                # 游戏结束
                winner, diff = self.board.get_winner()  # 得到赢家 0,1,2
                break
            # 否则游戏继续
            self.current_player = self.switch_player(self.current_player)
        # 当游戏结束，返回游戏结果
        return (winner, diff)

    def game_over(self):
        """
        判断游戏是否结束
        :return: True/False 游戏结束/游戏没有结束
        """

        # 根据当前棋盘，判断棋局是否终止
        # 如果当前选手没有合法下棋的位子，则切换选手；如果另外一个选手也没有合法的下棋位置，则比赛停止。
        b_list = list(self.board.get_legal_actions('X'))
        w_list = list(self.board.get_legal_actions('O'))

        is_over = len(b_list) == 0 and len(w_list) == 0  # 返回值 True/False

        return is_over