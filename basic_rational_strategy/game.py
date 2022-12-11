import numpy as np

class Agent:
    """
    This class defines the agent that 
    participates in the purgatory game.
    Each agent has a strategy type (0,F)
    """
    def __init__(self, strategy, index,args):
        self.strategy = strategy
        self.payment = strategy
        self.flag=False
        self.time=0
        self.index=index
        self.history=[index]
        if args.ignorance_distribution == 1:
            self.prob=np.random.uniform(args.p_min, 1)
        elif args.ignorance_distribution == 2:
            self.prob=args.prob
        elif args.ignorance_distribution == 3:
            self.prob=np.random.beta(args.a, args.b)
    def mutate(self,trend,fine):
        """
        Change of strategy based on trend.
        """
        if trend:
            if self.strategy < fine:
                self.strategy+=1
        else:
            if self.strategy > 0:
                self.strategy-=1
                      
class Game:
    '''
    This class stores and updates the 
    queue on which the purgatory game 
    is played.
    '''
    def __init__(self, args):
        Agents=[]
        n=args.n    
        for i in range(n):
            Agents.append(Agent(0,i,args))
            Heads= np.random.uniform(0, 1) > Agents[i].prob
            if Heads:
                Agents[i].payment+=1
                Agents[i].strategy+=1
        self.agents=Agents
        self.timelimit=args.T
        self.time=0
        self.pay=args.K
        self.prob=args.ignorance_distribution
        self.fine=args.F
        self.Q=args.Q
        self.collected=0
        self.x_mean=args.x_mean
        self.x_std=args.x_std
        self.args = args
    def sort(self):
        """
        Sort by ratio of payment and time spent. 
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
    def run(self):
        '''
        Run a single iteration of the game.
        First K agents are sent to hell 
        and forced to pay Q.
        Each agent pays his strategy
        with probability (1-probability of ignorance)
        Players ho have paid F or 
        spent T iterations are sent to heaven.
        The queue is sorted and new agents enter.
        '''
        F=self.fine
        Q=self.Q
        out=[]
        for agent in self.agents:
            act=np.random.uniform(0, 1) > agent.prob                            #probability with which agent checks the system and chooses to play
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
        
        
        n0=int(np.random.normal(self.x_mean,self.x_std))
        if n0 < 0:
            raise ValueError('Number of people entering the queue cannot be negative. Check the values of x_mean and x_std')
        for _ in range(n0):
            l=len(self.agents)
            prob=self.prob
            self.agents.append(Agent(0,l,self.args))
            Heads= np.random.uniform(0, 1) > self.agents[l].prob
            if Heads:
                self.agents[l].payment+=1
                self.agents[l].strategy+=1
        return self.collected, out
        