import copy
class AIPlayer_AlphaBeta:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color

    def get_value(self, board, action):
        [x,y] = board.board_num(action)
        value_chart = [
        [90,-60,10,10,10,10,-60,90],
        [-60,-80,5,5,5,5,-80,-60],
        [10,5,1,1,1,1,5,10],
        [10,5,1,1,1,1,5,10],
        [10,5,1,1,1,1,5,10],
        [10,5,1,1,1,1,5,10],
        [-60,-80,5,5,5,5,-80,-60],
        [90,-60,10,10,10,10,-60,90]
        ]
        return value_chart[x][y]
    
    def inv_color(self, now_color):
        if now_color == 'X':
            return 'O'
        else:
            return 'X'

    def min_value(self,board,max_depth,depth,action,a,b):
        now_color = self.inv_color(self.color) #判断最大值的时候肯定是对方下

        if depth > max_depth: #如果迭代深度达到要求
            return self.get_value(board, action)
        
        value_final = 100000000

        action_list = list(board.get_legal_actions(now_color))#获取所有合法位置
        if not len(action_list)==0:
            for action in action_list:
                board_next = copy.deepcopy(board) #复制一份地图
                board_next._move(action,now_color) #假如对手下在action这个位置
                value_max = self.max_value(board_next,max_depth,depth+1,action,a,b) #我们会下在对我们最有利的位置
                value_final = min(value_final,value_max)#那么对方会从中选对我们最差的一个
                if value_final<=a:
                    return value_final
                b = min(b,value_final)
            return value_final
        else:#如果已经没有地方进行落子的话
            return self.get_value(board, action)


    
    def max_value(self,board,max_depth,depth,action,a,b):
        now_color = self.color #判断最大值的时候肯定是己方下
        if depth > max_depth: #如果迭代深度达到要求
            return -1*self.get_value(board, action)
        
        value_final = -100000000

        action_list = list(board.get_legal_actions(now_color))#获取所有合法位置
        if not len(action_list)==0:
            for action in action_list:
                board_next = copy.deepcopy(board) #复制一份地图
                board_next._move(action,now_color) #假如自己下在action这个位置
                value_min = self.min_value(board_next,max_depth,depth+1,action,a,b) #对手会下在对我们而言最差的位置
                value_final = max(value_final,value_min)#从最差中找到综合来看对自己最有利的点
                if value_final>=b:
                    return value_final
                a = max(a,value_final)
            return value_final
        else:
            return -1*self.get_value(board, action)

    def alphabeta(self,board,max_depth):
        now_color = self.color
        value_final = -100000000
        a = -10000000
        b = 10000000
        depth = 0
        action_list = list(board.get_legal_actions(now_color)) #获取当前自己能下的所有点
        action_final = action_list[0]
        for action in action_list:
            board_next = copy.deepcopy(board) #复制一份地图
            board_next._move(action,now_color) #假如下在action这个位置
            value_min = self.min_value(board_next,max_depth,depth+1,action,a,b) #对手会下在对我们而言最差的位置
            if value_min > value_final:# 从最差中找到综合来看对自己最有利的点
                value_final = value_min
                action_final = action
        return action_final

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        
        depth = 3 #定义搜索深度
        action = self.alphabeta(board, depth)
        print(action)
        # ------------------------------------------------------------------------

        return action
