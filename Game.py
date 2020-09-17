import re
import time
import copy
import random
class  TicTacToe:

  def __init__(self, n, k , mode):
    self.field=[['.' for i in range(n)] for j in range(n)]
    self.size=n
    self.dlina=k
    self.laststep=(0,0)
    if (mode=='pvp'):
      self.player1=Human(1)
      self.player2=Human(2)
    elif (mode=='pvai'):
      self.player1=Human(1)
      self.player2=Ai(2)
    elif (mode=='aivai'):
      self.player1=Ai(1)
      self.player2=Ai(2)
    else:
      print('Invalid mode')
    self.nowstep=self.player1
    self.player1.symbol='x'
    self.nextstep=self.player2
    self.player2.symbol='o'

  def show(self):
    nums='  '
    for k in range(self.size):
      nums+=str(k)+' '
    print(nums)
    for i in range(self.size):
      st=str(i)+ ' '
      for j in range(self.size):
        st+=self.field[i][j]+' '
      print(st)

  def make_step(self):
    self.laststep=self.nowstep.choose_step(self)
    self.field[self.laststep[0]][self.laststep[1]]=self.nowstep.symbol
    self.nowstep, self.nextstep = self.nextstep, self.nowstep

  def play(self):
    print('start of the game')
    while (self.check_if_win()==False):
      self.show()
      time.sleep(1)
      self.make_step()
    self.show()
    print('Player {} won the game'.format(self.nextstep))

  def check_if_win(self):
    strings=self.makestrings(self.laststep[0], self.laststep[1])
    winreg=re.compile('{}'.format(self.nextstep.symbol)+'{'+'{}'.format(self.dlina)+',}')
    if (any(re.search(winreg, line) for line in strings)):
      return True
    else:
      return False
  def makestrings(self, x, y):
    st=['']*4
    for j in range(self.size):
      st[0]+=self.field[x][j]
    for i in range(self.size):
      st[1]+=self.field[i][y]
    if (x>y):
      for i in range(x-y, self.size):
        st[2]+=self.field[i][i-(x-y)]
    else:
      for i in range(self.size-(y-x)):
        st[2]+=self.field[i][i+(y-x)]
    if ((y+x)>self.size-1):
      for i in range((y+x)-self.size+1, self.size):
        st[3]+=self.field[i][(y+x)-i]
    else:
      for i in range((y+x)+1):
        st[3]+=self.field[i][(y+x)-i]
    return st


class Human:
  def __init__(self, num):
    self.num=num
    self.symbol=''
  def choose_step(self, game: TicTacToe):
    print('Player {} choose step'.format(self.num))
    x=int(input("Print line number: "))
    y=int(input("Print column number: "))
    if (game.field[x][y]!='.'):
      print('Invalid')
      return None
    return (x,y)

class Ai:
  def __init__(self,num):
    self.num=num
    self.symbol=''
  def choose_step(self, game: TicTacToe):
    print('Player ai{} choose step'.format(self.num))
    steps=[]
    reg=[None]*8
    for i in range(game.size):
      for j in range(game.size):
        if (game.field[i][j]!='.'):
          for k in range(i-1,i+2):
            for m in range(j-1,j+2):
              if ((k in range(game.size))&(m in range(game.size))):
                  if (game.field[k][m]=='.'):
                      steps.append((k,m))
    reg[0]=re.compile('.a' + game.nowstep.symbol + '+.')
    reg[1]=re.compile('.' + game.nowstep.symbol + '+a.')
    reg[2]=re.compile(game.nextstep.symbol + '((a' + game.nowstep.symbol + '+)|' + '(' + game.nowstep.symbol + '+a))')
    reg[3]=re.compile('((a' + game.nowstep.symbol + '+)|' + '(' + game.nowstep.symbol + '+a))' + game.nextstep.symbol)
    reg[4]=re.compile(game.nowstep.symbol + game.nextstep.symbol + '+a')
    reg[5]=re.compile('a' + game.nextstep.symbol + '+' + game.nowstep.symbol)
    reg[6]=re.compile('\.' + game.nextstep.symbol + '+a')
    reg[7]=re.compile('a' + game.nextstep.symbol + '+\.')
    scores={}
    for step in steps:
      train = copy.deepcopy(game)
      train.field[step[0]][step[1]]='a'
      strings=train.makestrings(step[0], step[1])
      maxi=0
      for string in strings:
        score=0
        if ((list(string).count('.')+list(string).count('x')>=train.dlina) or (list(string).count('.')+list(string).count('o')>=train.dlina)):
          for u in range(8):
            try:
              if (u<=1):
                score+=list(re.search(reg[u], string).group()).count(train.nowstep.symbol)**2*10
              elif (u<=3):
                score+=list(re.search(reg[u], string).group()).count(train.nowstep.symbol)**2*6
              elif (u<=5):
                score+=list(re.search(reg[u], string).group()).count(train.nextstep.symbol)**2*10
              else:
                score+=list(re.search(reg[u], string).group()).count(train.nextstep.symbol)**2*6
            except:
              pass
        if (score>maxi):
          maxi=score
      scores[step]=maxi+random.random()
    try:
      return max(scores.items(),key = lambda x:x[1])[0]
    except:
      return (int(game.size/2), int(game.size/2))