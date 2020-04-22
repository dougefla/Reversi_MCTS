import json
import numpy
import random
import copy
import math
import time
import datetime

timeout = 3

class Board(object):
    """
    Board 黑白棋棋盘，规格是8*8，黑棋用 X 表示，白棋用 O 表示，未落子时用 . 表示。
    """

    def __init__(self):
        """
        初始化棋盘状态
        """
        self.empty = '.'  # 未落子状态
        self._board = [[self.empty for _ in range(8)] for _ in range(8)]  # 规格：8*8
        self._board[3][4] = 'X'  # 黑棋棋子
        self._board[4][3] = 'X'  # 黑棋棋子
        self._board[3][3], self._board[4][4] = 'O', 'O'  # 白棋棋子

    def __getitem__(self, index):
        """
        添加Board[][] 索引语法
        :param index: 下标索引
        :return:
        """
        return self._board[index]

    def display(self, step_time=None, total_time=None):
        """
        打印棋盘
        :param step_time: 每一步的耗时, 比如:{"X":1,"O":0},默认值是None
        :param total_time: 总耗时, 比如:{"X":1,"O":0},默认值是None
        :return:
        """
        board = self._board
        # print(step_time,total_time)
        # 打印列名
        print(' ', ' '.join(list('ABCDEFGH')))
        # 打印行名和棋盘
        for i in range(8):
            # print(board)
            print(str(i + 1), ' '.join(board[i]))
        if (not step_time) or (not total_time):
            # 棋盘初始化时展示的时间
            step_time = {"X": 0, "O": 0}
            total_time = {"X": 0, "O": 0}
            print("统计棋局: 棋子总数 / 每一步耗时 / 总时间 ")
            print("黑   棋: " + str(self.count('X')) + ' / ' + str(step_time['X']) + ' / ' + str(
                total_time['X']))
            print("白   棋: " + str(self.count('O')) + ' / ' + str(step_time['O']) + ' / ' + str(
                total_time['O']) + '\n')
        else:
            # 比赛时展示时间
            print("统计棋局: 棋子总数 / 每一步耗时 / 总时间 ")
            print("黑   棋: " + str(self.count('X')) + ' / ' + str(step_time['X']) + ' / ' + str(
                total_time['X']))
            print("白   棋: " + str(self.count('O')) + ' / ' + str(step_time['O']) + ' / ' + str(
                total_time['O']) + '\n')

    def count(self, color):
        """
        统计 color 一方棋子的数量。(O:白棋, X:黑棋, .:未落子状态)
        :param color: [O,X,.] 表示棋盘上不同的棋子
        :return: 返回 color 棋子在棋盘上的总数
        """
        count = 0
        for y in range(8):
            for x in range(8):
                if self._board[x][y] == color:
                    count += 1
        return count

    def get_winner(self):
        """
        判断黑棋和白旗的输赢，通过棋子的个数进行判断
        :return: 0-黑棋赢，1-白旗赢，2-表示平局，黑棋个数和白旗个数相等
        """
        # 定义黑白棋子初始的个数
        black_count, white_count = 0, 0
        for i in range(8):
            for j in range(8):
                # 统计黑棋棋子的个数
                if self._board[i][j] == 'X':
                    black_count += 1
                # 统计白旗棋子的个数
                if self._board[i][j] == 'O':
                    white_count += 1
        if black_count > white_count:
            # 黑棋胜
            return 0, black_count - white_count
        elif black_count < white_count:
            # 白棋胜
            return 1, white_count - black_count
        elif black_count == white_count:
            # 表示平局，黑棋个数和白旗个数相等
            return 2, 0

    def _move(self, action, color):
        """
        落子并获取反转棋子的坐标
        :param action: 落子的坐标 可以是 D3 也可以是(2,3)
        :param color: [O,X,.] 表示棋盘上不同的棋子
        :return: 返回反转棋子的坐标列表，落子失败则返回False
        """
        # 判断action 是不是字符串，如果是则转化为数字坐标
        if isinstance(action, str):
            action = self.board_num(action)

        fliped = self._can_fliped(action, color)

        if fliped:
            # 有就反转对方棋子坐标
            for flip in fliped:
                x, y = self.board_num(flip)
                self._board[x][y] = color

            # 落子坐标
            x, y = action
            # 更改棋盘上 action 坐标处的状态，修改之后该位置属于 color[X,O,.]等三状态
            self._board[x][y] = color
            return fliped
        else:
            # 没有反转子则落子失败
            return False

    def backpropagation(self, action, flipped_pos, color):
        """
        回溯
        :param action: 落子点的坐标
        :param flipped_pos: 反转棋子坐标列表
        :param color: 棋子的属性，[X,0,.]三种情况
        :return:
        """
        # 判断action 是不是字符串，如果是则转化为数字坐标
        if isinstance(action, str):
            action = self.board_num(action)

        self._board[action[0]][action[1]] = self.empty
        # 如果 color == 'X'，则 op_color = 'O';否则 op_color = 'X'
        op_color = "O" if color == "X" else "X"

        for p in flipped_pos:
            # 判断action 是不是字符串，如果是则转化为数字坐标
            if isinstance(p, str):
                p = self.board_num(p)
            self._board[p[0]][p[1]] = op_color

    def is_on_board(self, x, y):
        """
        判断坐标是否出界
        :param x: row 行坐标
        :param y: col 列坐标
        :return: True or False
        """
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def _can_fliped(self, action, color):
        """
        检测落子是否合法,如果不合法，返回 False，否则返回反转子的坐标列表
        :param action: 下子位置
        :param color: [X,0,.] 棋子状态
        :return: False or 反转对方棋子的坐标列表
        """
        # 判断action 是不是字符串，如果是则转化为数字坐标
        if isinstance(action, str):
            action = self.board_num(action)
        xstart, ystart = action

        # 如果该位置已经有棋子或者出界，返回 False
        if not self.is_on_board(xstart, ystart) or self._board[xstart][ystart] != self.empty:
            return False

        # 临时将color放到指定位置
        self._board[xstart][ystart] = color
        # 棋手
        op_color = "O" if color == "X" else "X"

        # 要被翻转的棋子
        flipped_pos = []
        flipped_pos_board = []

        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                                       [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            # 如果(x,y)在棋盘上，而且为对方棋子,则在这个方向上继续前进，否则循环下一个角度。
            if self.is_on_board(x, y) and self._board[x][y] == op_color:
                x += xdirection
                y += ydirection
                # 进一步判断点(x,y)是否在棋盘上，如果不在棋盘上，继续循环下一个角度,如果在棋盘上，则进行while循环。
                if not self.is_on_board(x, y):
                    continue
                # 一直走到出界或不是对方棋子的位置
                while self._board[x][y] == op_color:
                    # 如果一直是对方的棋子，则点（x,y）一直循环，直至点（x,y)出界或者不是对方的棋子。
                    x += xdirection
                    y += ydirection
                    # 点(x,y)出界了和不是对方棋子
                    if not self.is_on_board(x, y):
                        break
                # 出界了，则没有棋子要翻转OXXXXX
                if not self.is_on_board(x, y):
                    continue

                # 是自己的棋子OXXXXXXO
                if self._board[x][y] == color:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        # 回到了起点则结束
                        if x == xstart and y == ystart:
                            break
                        # 需要翻转的棋子
                        flipped_pos.append([x, y])

        # 将前面临时放上的棋子去掉，即还原棋盘
        self._board[xstart][ystart] = self.empty  # restore the empty space

        # 没有要被翻转的棋子，则走法非法。返回 False
        if len(flipped_pos) == 0:
            return False

        for fp in flipped_pos:
            flipped_pos_board.append(self.num_board(fp))
        # 走法正常，返回翻转棋子的棋盘坐标
        return flipped_pos_board

    def get_legal_actions(self, color):
        """
        按照黑白棋的规则获取棋子的合法走法
        :param color: 不同颜色的棋子，X-黑棋，O-白棋
        :return: 生成合法的落子坐标，用list()方法可以获取所有的合法坐标
        """
        # 表示棋盘坐标点的8个不同方向坐标，比如方向坐标[0][1]则表示坐标点的正上方。
        direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        op_color = "O" if color == "X" else "X"
        # 统计 op_color 一方邻近的未落子状态的位置
        op_color_near_points = []

        board = self._board
        for i in range(8):
            # i 是行数，从0开始，j是列数，也是从0开始
            for j in range(8):
                # 判断棋盘[i][j]位子棋子的属性，如果是op_color，则继续进行下一步操作，
                # 否则继续循环获取下一个坐标棋子的属性
                if board[i][j] == op_color:
                    # dx，dy 分别表示[i][j]坐标在行、列方向上的步长，direction 表示方向坐标
                    for dx, dy in direction:
                        x, y = i + dx, j + dy
                        # 表示x、y坐标值在合理范围，棋盘坐标点board[x][y]为未落子状态，
                        # 而且（x,y）不在op_color_near_points 中，统计对方未落子状态位置的列表才可以添加该坐标点
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x][y] == self.empty and (
                                x, y) not in op_color_near_points:
                            op_color_near_points.append((x, y))
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        for p in op_color_near_points:
            if self._can_fliped(p, color):
                # 判断p是不是数字坐标，如果是则返回棋盘坐标
                # p = self.board_num(p)
                if p[0] in l and p[1] in l:
                    p = self.num_board(p)
                yield p

    def board_num(self, action):
        """
        棋盘坐标转化为数字坐标
        :param action:棋盘坐标，比如A1
        :return:数字坐标，比如 A1 --->(0,0)
        """
        row, col = str(action[1]).upper(), str(action[0]).upper()
        if row in '12345678' and col in 'ABCDEFGH':
            # 坐标正确
            x, y = '12345678'.index(row), 'ABCDEFGH'.index(col)
            return x, y

    def num_board(self, action):
        """
        数字坐标转化为棋盘坐标
        :param action:数字坐标 ,比如(0,0)
        :return:棋盘坐标，比如 （0,0）---> A1
        """
        row, col = action
        l = [0, 1, 2, 3, 4, 5, 6, 7]
        if col in l and row in l:
            return chr(ord('A') + col) + str(row + 1)
    def is_game_ended(self):
        return not self.get_legal_actions('X') and not self.get_legal_actions('O')

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

# Node类是状态，代表一种局势
class Node(object):
    def __init__(self):
        # 上一步棋对应的局势
        self.parent = None
        # 下一步棋对应的局势，以{sub_node:action}形式存储
        self.children = {}
        # 在MCTS随机搜索过程中，被访问过的次数
        self.visit_times = 0
        # 这种局势的评分
        self.quality_value = 0.0
        # 当前轮数。第一手为1
        self.round_index = 0
        # 初始化棋盘
        self.board_ = [['.' for _ in range(8)] for _ in range(8)]
        self.board_[3][4] = 'X'  # 黑棋棋子
        self.board_[4][3] = 'X'  # 黑棋棋子
        self.board_[3][3], self.board_[4][4] = 'O', 'O'  # 白棋棋子
        # 在该局面下，将要下棋一方的颜色，'X'为黑，'O'为白
        self.color = 'X'

    # 获取对手颜色
    def oppsite_color(self,color):
        if color=='X':
            return 'O'
        else:
            return 'X'

    # 根据Node获得Board类的实例board
    def get_formate_board(self):
        formate_board = Board()
        for i in range(8):
            for j in range(8):
                formate_board._board[i][j] = self.board_[i][j]
        return formate_board

    # 获取当前局势下，可以做的action
    def get_valid_actions(self,color):
        # Board类提供了相关算法，所以先转化到Board类
        format_board = self.get_formate_board()
        # 调用Board类的方法，获得可以做的action
        actions = list(format_board.get_legal_actions(color))
        return actions

    # 根据action更新节点局面
    def update_node_with_action(self,action,color):
        format_board = self.get_formate_board()
        format_board._move(action,color)
        for i in range(8):
            for j in range(8):
                self.board_[i][j] = format_board._board[i][j] 

    # 根据Board类的实例board初始化Node
    def initiate_node_with_board(self,format_board):
        for i in range(8):
            for j in range(8):
                self.board_[i][j] = format_board._board[i][j]

    def is_all_expand(self):
        if len(self.get_valid_actions(self.color)) == len(self.children):
            return True
        else:
            return False
    def print_children(self):
        for node in self.children:
            print(node.visit_times)
    # 用于子节点继承父节点的局面
    def born_from(self,node):
        self.board_ = copy.deepcopy(node.board_)
        self.color = self.oppsite_color(node.color)
        self.round_index = node.round_index + 1


class MCTS(object):
    def __init__(self, board, color):
        # 这是总棋盘,在一次查询中不会进行更改，使用前必须deepcopy
        self.board = board
        # 这是我方颜色，不会变化
        self.mycolor = color
    def MCTS_search(self,root_node):
        root_node.color = self.mycolor
        if len(root_node.get_valid_actions(root_node.color))==0:
            return -1
        
        # 获取当前时间
        start_time = time.perf_counter()
        # 迭代直到到达时间限制
        while time.perf_counter() - start_time < timeout:
            # 根据TreePolicy对树进行扩展，也就是下一步棋
            expand_node = self.tree_policy(root_node)
            # 对扩展出的局势进行仿真，计算评分
            reward = self.default_policy(expand_node)
            # 把这个评分返回所有路径上的节点
            self.backup(expand_node, reward)
        # 当时间到，从已经访问过的节点中选一个评分最高的返回对应action
        best_node = self.best_child(root_node,0)
        return root_node.children[best_node]
    
    # 树的维护算法
    def tree_policy(self,node):
        # 当前节点仍可以下棋时：
        while self.is_terminal(node)==False:
            # 如果当前节点未被探索过
            if not node.is_all_expand():
                # 随机返回一个还没探索过的新节点
                sub_node = self.expand(node)
                return sub_node
            else:
                # 否则就从子节点中找一个最好，重新开始
                node = self.best_child(node,1/math.sqrt(2.0))
                continue
        return node

    # 随机返回新节点
    def expand(self,node):
        # 根据当前的局势获得可能的action
        action_list = node.get_valid_actions(node.color)
        action = random.choice(action_list)
        
        # 找一个没有探索过的
        while action in node.children.values():
            action = random.choice(action_list)
        # 根据action构建新node
        sub_node = Node()
        sub_node.born_from(node)
        sub_node.update_node_with_action(action,node.color)
        # 把新node添加到原node的children中
        node.children[sub_node]=action
        sub_node.parent = node
        return sub_node
    
    # 根据当前局势进行仿真。使用快速走子策略进行，此处我们使用Random进行快速仿真
    def default_policy(self,node):
        temp_node = copy.deepcopy(node)
        game = Random_Game(temp_node.board_,temp_node.color)
        # 获得游戏结果
        (winner,diff) = game.run()
        # 如果是我方获得胜利，返回1；否则（输或平局）返回0；
        if (winner==0 and self.mycolor=='X') or (winner==1 and self.mycolor=='O'):
            reward = 1
        else:
            reward = 0
        return reward
    
    # 反向传播算法
    def backup(self,node,reward):
        # 从当前节点开始，向上传递
        while node!=None:
            # 将当前节点访问次数+1
            node.visit_times+=1
            # 更新当前节点评分
            node.quality_value+=reward
            # 切换到父节点
            node = node.parent
    
    # UCB算法，取置信上限最高的节点。Cp是参数
    def best_child(self,node,Cp):
        best_node = node
        max_value = -100000
        for sub_node in node.children.keys():
            # 如果是轮到我方下棋，那么胜率正常计算
            if node.color == self.mycolor:
                value = sub_node.quality_value/sub_node.visit_times+Cp*math.sqrt(2*math.log(node.visit_times)/sub_node.visit_times)
            # 如果是轮到对方下棋，那么胜率要反过来
            else:
                value = (1-sub_node.quality_value/sub_node.visit_times)+Cp*math.sqrt(2*math.log(node.visit_times)/sub_node.visit_times)
            if value>max_value:
                best_node = sub_node
                max_value = value
        return best_node
    # 当本方不能下棋，就不再扩展该树
    def is_terminal(self,node):
        if len(node.get_valid_actions(node.color)) == 0:
            return True
        else:
            return False

class AIPlayer_MCTS:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        mcts = MCTS(board,self.color)
        root_node = Node()
        root_node.initiate_node_with_board(board)
        action = mcts.MCTS_search(root_node)
        return action

# 初始化棋盘
def initBoard():
    board = numpy.zeros((8, 8), dtype=numpy.int)
    board[3][4] = board[4][3] = 1
    board[3][3] = board[4][4] = -1
    return board

def main():
    #初始化棋盘
    board = Board()

    #获得第一次输入
    fullInput = json.loads(input())
    requests = fullInput["requests"]
    #分析第一次输入
    myColor = 'X'
    hisColor = 'O'
    #如果第一次输入是合法的，说明对面执黑，输入的是对面的第一次落子
    if requests[0]["x"] >= 0:
        x_2 = requests[0]['x']
        y_2 = requests[0]['y']
        myColor = 'O'
        hisColor = 'X'
        his_action = (x_2,y_2)
        #根据对方的输入修改棋盘
        board._move(his_action,hisColor)
    #否则说明我们执黑
    #创建Bot，使用MCTS算法
    Bot = AIPlayer_MCTS(myColor)
    #使用长时间运行模式，直到游戏结束
    while not board.is_game_ended():
        board_temp = copy.deepcopy(board)
        action = Bot.get_move(board_temp)
        #如果无子可下，就输出(-1,-1)
        if action==-1:
            print(json.dumps({"response": {"x": -1, "y": -1}}))
            print('\n>>>BOTZONE_REQUEST_KEEP_RUNNING<<<\n', flush=True)
        #否则修改棋盘，并输出信息
        else:
            (x,y) = board.board_num(action)
            board._move(action,myColor)
            print(json.dumps({"response": {"x": x, "y": y}}))
            print('\n>>>BOTZONE_REQUEST_KEEP_RUNNING<<<\n', flush=True)

        #读取数据
        fullInput = json.loads(input())
        #获得对方上一步信息
        x_2 = fullInput['x']
        y_2 = fullInput['y']
        #如果对方没有跳步
        if x_2 >= 0:
            his_action = (x_2,y_2)
            #根据对方的输入修改棋盘
            board._move(his_action,hisColor)
        #如果跳步了，就直接继续下

main()