
"""
수렴할 때까지 n번 반복
한 에피소드의 경험을 쌓고
경험한 데이터로 q(s,a) 테이블의 값을 업데이트하고 (정책 평가)
업데이트된 q(s,a) 테이블을 이용하여 epsilon-greedy 정책을 만든다. (정책 개선)
"""

import random
import numpy as np

class GridWorld():
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def step(self, a):
        if a == 0:
            self.move_left()
        elif a == 1:
            self.move_up()
        elif a == 2:
            self.move_right()
        elif a == 3:
            self.move_down()

        reward = -1
        done = self.is_done()
        return (self.x, self.y), reward, done

    def move_left(self):
        if self.y == 0:
            pass
        elif self.y == 3 and self.x in [0,1,2]:
            pass
        elif self.y == 5 and self.x in [2,3,4]:
            pass
        else:
            self.y -= 1

    def move_right(self):
        if self.y == 1 and self.x in [0,1,2]:
            pass
        elif self.y == 3 and self.x in [2,3,4]:
            pass
        elif self.y == 6:
            pass
        else:
            self.y +=1
    
    def move_up(self):
        if self.x == 0:
            pass
        elif self.x == 3 and self.y == 2:
            pass
        else:
            self.x -= 1
    
    def move_down(self):
        if self.x == 4:
            pass
        elif self.x == 1 and self.y == 4:
            pass
        else:
            self.x += 1

    def is_done(self):
        if self.x==4 and self.y == 6:
            return True
        else:
            return False

    def reset(self):
        self.x = 0
        self.y = 0
        return (self.x, self.y)

class QAgent():
    def __init__(self):
        self.q_table = np.zeros((5,7,4)) # q-value를 저장하는 변수, 모두 0으로 초기화
        # x= 5칸, y= 7칸, 각각 4방향 action에 대한 q값
        self.eps = 0.9

    def select_action(self, s):
        # eps-greedy로 액션을 선택한다.
        x, y = s
        coin = random.random()
        if coin < self.eps:
            action = random.randint(0,3)
        else:
            action_val = self.q_table[x,y,:]
            action = np.argmax(action_val)
        return action
    
    def update_table(self, transition):
        s, a, r, s_prime = transition
        x,y = s
        next_x, next_y = s_prime
        
        # using Q-Learning update formula
        self.q_table[x,y,a] = self.q_table[x,y,a]+ 0.1 * (r+np.amax(self.q_table\
            [next_x,next_y,:]) - self.q_table[x,y,a])

    def anneal_eps(self):
        self.eps -= 0.01
        self.eps = max(self.eps, 0.2)

    def show_table(self):
        # 학습이 각 위치에서 어느 액션의 q 값이 가장 높은지 보여주는 함수
        q_lst = self.q_table.tolist()
        data = np.zeros((5,7))
        for row_idx in range(len(q_lst)):
            row = q_lst[row_idx]
            for col_idx in range(len(row)):
                col = row[col_idx]
                action = np.argmax(col)
                data[row_idx, col_idx] = action
        print(data)

def main():
    env = GridWorld()
    agent = QAgent()

    for n_epi in range(10000):
        done = False

        s = env.reset()
        while not done:
            a = agent.select_action(s)
            s_prime, r, done = env.step(a)
            agent.update_table((s,a,r,s_prime))
            s = s_prime
        agent.anneal_eps()

    agent.show_table()

if __name__ == '__main__':
    main()