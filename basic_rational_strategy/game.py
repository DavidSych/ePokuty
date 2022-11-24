import numpy as np
import random
import pandas as pd
import os.path
import struct
import h5py
from bisect import bisect_left
import re

class Agent:
    def __init__(self, strategy, index,prob):
        """
        Each agent has a strategy type (0,F)
        And starting fitness as per position
        """
        self.strategy = strategy
        self.payment = strategy
        self.payoff=0
        self.flag=False
        self.time=0
        self.index=index
        self.history=[index]
        self.prob=prob
    def mutate(self,trend,fine):
        """
        Allow a small chance of mutation to flip strategy
        Otherwise, return offspring of the same type
        """
        if trend:
            if self.strategy < fine:
                self.strategy+=1
        else:
            if self.strategy > 0:
                self.strategy-=1
                      
class Game:
    def __init__(self, n,F,Q, T, K,prob):
        Agents=[]
        for i in range(n):
            Agents.append(Agent(0,i,prob))
            Heads= random.randint(1,1000) > Agents[i].prob
            if Heads:
                Agents[i].payment+=1
                Agents[i].strategy+=1
        self.agents=Agents
        self.timelimit=T
        self.time=0
        self.pay=K
        self.prob=prob
        self.fine=F
        self.Q=Q
        self.collected=0
    def sort(self):
        """
        Sort by payment
        """
        c=self.timelimit/10
        for agent in self.agents:
            if agent.flag:
                print(agent.index,agent.payment,agent.time)
        self.agents.sort(key=lambda x: ((x.payment+c)/x.time), reverse=False)
        for agent in self.agents:
            agent.index=self.agents.index(agent)
            agent.history.append(agent.index)
    def trend(self,agent):
        T=self.timelimit
        rate=agent.strategy
        pos=agent.index
        t=agent.time
        if t > 10:
            return (agent.history[t-10]-agent.history[t])*(T-t)/10.0 > pos
        else:
            return (agent.history[0]-agent.history[t])*(T-t)/t > pos                                                #agent likely to have to pay
    def payment(self):
        sum = 0
        for agent in self.agents:
            sum+=agent.payment
        return sum
    def run(self):
        #act=random.randint(0,1000)>100
        F=self.fine
        Q=self.Q
        out=[]
        for agent in self.agents:
            act=random.randint(0,1000) > agent.prob                            #probability with which agent checks the system and chooses to play
            if agent.index < self.pay:
                agent.flag=True                                        #first K agents marked for removal
                if agent.payment < F:
                    agent.payment= agent.payment + Q
                    self.collected+=Q
            elif act:
                if agent.payment < F:
                    delta=min(agent.strategy,F-agent.payment)
                    agent.payment=agent.payment+delta            #if agent chooses to play his payment increases as per his strategy
                    self.collected+=delta
            if agent.payment >= F:
                agent.flag=True
            agent.time+=1
            if agent.time >= self.timelimit:
                agent.flag=True
        self.time+=1
        
        Agents=[agent for agent in self.agents if not agent.flag]
        out=[agent for agent in self.agents if agent.flag and agent.index > self.pay]
        self.agents=Agents
        self.sort()
        for agent in self.agents:
               if agent.time > 0:
                   trend=self.trend(agent)
                   agent.mutate(trend,F)
        
        
        n0=int(np.random.normal(100,15))
        for _ in range(n0):
            l=len(self.agents)
            prob=self.prob
            self.agents.append(Agent(0,l,prob))
            Heads= random.randint(1,1000) > self.agents[l].prob
            if Heads:
                self.agents[l].payment+=1
                self.agents[l].strategy+=1
        return self.collected, out
        