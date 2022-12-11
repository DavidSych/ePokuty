from game import Game
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gc
import os 
import argparse
import datetime

parse = argparse.ArgumentParser()

parse.add_argument("--seed", default=42, type=int, help="Seed for random sampling")
parse.add_argument("--n", default=1000, type=int, help="Length of queue at the beginning of the game")
parse.add_argument("--F", default=50, type=int, help="Fine to pay for going to heaven.")
parse.add_argument("--Q", default=0, type=int, help="Additional penalty for going to hell.")
parse.add_argument("--T", default=100, type=int, help="Time to survive in queue for going to heaven.")
parse.add_argument("--K", default=5, type=int, help="How many people go to hell in each time step.")
parse.add_argument("--x_mean", default=100, type=float, help="Mean number of people entering the queue at each time step.")
parse.add_argument("--x_std", default=15, type=float, help="Standard deviation of the number of people entering the queue at each time step.")
parse.add_argument("--ignorance_distribution", default=1, type=int, help="Distribution to use to sample probability of ignorance for each player. Supported: 1 (uniform), 2 (fixed), 3 (beta).")
parse.add_argument("--prob", default=0.7, type=float, help="Probability of ignorance, if fixed.")
parse.add_argument("--p_min", default=0.7, type=float, help="Minimum probability of ignorance, if uniform.")
parse.add_argument("--a", default=7, type=float, help="Shape parameter of Beta(a,b) distribution for sampling probability ignorance.")
parse.add_argument("--b", default=3, type=float, help="Shape parameter of Beta(a,b) distribution for sampling probability of ignorance.")
parse.add_argument("--total_time", default=10000, type=int, help="How many time steps to run")

args = parse.parse_args([] if "__file__" not in globals() else None)

if args.n < args.K:
    raise ValueError('Everyone cannot go to hell')
if args.prob > 1:
    raise ValueError('Probability cannot be greater than 1')
if args.prob < 0:
    raise ValueError('Probability cannot be negative')
if args.p_min < 0:
    raise ValueError('Probability cannot be negative')
if args.p_min > 1:
    raise ValueError('Probability cannot be greater than 1')
if args.a < 0:
    raise ValueError('Shape parameter of Beta distribution cannot be negative')
if args.b < 0:
    raise ValueError('Shape parameter of Beta distribution cannot be negative')
if args.ignorance_distribution < 1:
    raise ValueError("ignorance_distribution must be 1,2 or 3") 
if args.ignorance_distribution > 3:
    raise ValueError("ignorance_distribution must be 1,2 or 3") 
if args.total_time < 1:
    raise ValueError("Cannot run zero or negative iterations") 

np.random.seed(args.seed)

def main():
    title=[]
    F=args.F
    for k in range(F+1):
        strx="n_{}".format(k)+"_prop"
        title.append(strx)
    game=Game(args)
    rows = []
    zeropayment=0
    for i in range(args.total_time):
        print(i,'\t',len(game.agents))
        strategy = [agent.strategy for agent in game.agents]
        M=len(game.agents)-5
        extras = game.agents[-M:]
        first5 = game.agents[:5]
        payment5 = [agent.payment for agent in first5]
        time5 = [agent.time for agent in first5]
        row={}
        for j in range(F+1):
            strx="n_{}".format(j)
            row[strx]=strategy.count(j)
            row[strx+"_prop"]=strategy.count(j)*100/len(strategy)
        row['game_size']=len(strategy) 
        row['average payment of hell bound players']=np.mean(payment5)
        row['average time spent by hell bound players']=np.mean(time5)
        collected, out=game.run()
        if out:
            paymentout = [agent.payment for agent in out]
            zeropayment+=paymentout.count(0)
            timeout = [agent.time for agent in out]
            if i>0:
                ratioout = [agent.payment/agent.time for agent in out]
                row['average_ratio']=np.mean(ratioout)
            row['average payment of heaven bound players']=np.mean(paymentout)
            row['average time spent by heaven bound players']=np.mean(timeout)
            row['number of heaven bound players']=len(out)
        row['money collected']=collected
        rows.append(row)
    print('Total money collected:', collected)
    print('Average money collected per iteration:', collected/args.total_time)
    print('Average number of players who go to heaven without paying anything in a single iteration:', zeropayment/args.total_time)
    tit=''
    if args.ignorance_distribution ==1:
        tit="Probability of ignorance sampled uniformly at random from [{},1]".format(args.p_min)
    elif args.ignorance_distribution ==2:
        tit="Probability of ignorance  = {}".format(args.prob)
    elif args.ignorance_distribution ==3:
        tit=f"Probability of ignorance sampled from $ \\beta ({args.a},{args.b}) $"
    if not os.path.isdir('Results'):
        os.mkdir('Results')
    directory = f'd{str(datetime.datetime.now().date()).replace("-", "")}t{str(datetime.datetime.now().time())[:5].replace(":", "")}'
    os.mkdir('./Results/'+directory)
    df = pd.DataFrame(rows)
    strx="game.csv"
    df.to_csv(strx)
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(1.*i/(len(title)-1)) for i in range(len(title))]
    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=0,vmax=F))
    sm._A = [] 
    fig = df.plot(title=tit, y=title,color=colors,xlabel='time',ylabel='preferred actions for players by proportion',kind='area',legend=False)
    plt.colorbar(sm)
    strpdf="./Results/"+directory+"/game_strategies.png"
    fig.figure.savefig(strpdf,bbox_inches='tight')
    fig1 = df.plot(title=tit+"\n(The red line shows the average over all iterations)", y=["game_size"],grid=True,xlabel='time',figsize=(12.8,4.8),ylabel='size of queue',legend=False,linewidth=0.5)
    fig1.axhline(df["game_size"].mean(),c='r')
    strpdf1="./Results/"+directory+"/game_size.png"
    fig1.figure.savefig(strpdf1)
    fig2 = df.plot(title=tit, y=["average payment of hell bound players","average time spent by hell bound players"],xlabel='time',linewidth=0.5,grid=True,figsize=(12.8,4.8))
    strpdf2="./Results/"+directory+"/game_first_5.png"
    fig2.figure.savefig(strpdf2)
    fig3 = df.plot(title=tit, y=["average_ratio"],xlabel='time',ylabel='average ratio of payment and time spent by an agent',legend=False,linewidth=0.5,grid=True,figsize=(12.8,4.8))
    strpdf3="./Results/"+directory+"/game_agentratio.png"
    fig3.figure.savefig(strpdf3)
    fig4 = df.plot(title=tit, y=["number of heaven bound players","average time spent by heaven bound players"],grid=True,xlabel='time',figsize=(12.8,4.8),linewidth=0.5)
    strpdf4="./Results/"+directory+"/game_exitersstat.png"
    fig4.figure.savefig(strpdf4)
    fig5 = df.plot(title=tit, y=["average payment of heaven bound players"],xlabel='time',ylabel='Average payment of heaven bound players',legend=False,linewidth=0.5,grid=True,figsize=(12.8,4.8))
    strpdf5="./Results/"+directory+"/game_exiterspayment.png"
    fig5.figure.savefig(strpdf5)
    fig6 = df.plot(title=tit, y=["money collected"],grid=True,xlabel='time',ylabel='total money collected',legend=False,linewidth=0.5,figsize=(12.8,4.8))
    plt.yticks(rotation=90)
    strpdf5="./Results/"+directory+"/money_collected.png"
    fig6.figure.savefig(strpdf5)
    #fig1.close()
    plt.close('all')
    del df,row,rows
    gc.collect()
    if os.path.exists("game.csv"):
        os.remove("game.csv")

        

if __name__ == "__main__":
    main()
