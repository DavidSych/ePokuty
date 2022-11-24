from game import Game
import random
import numpy as np
import pandas as pd
#import matplotlib
import matplotlib.pyplot as plt
import statistics
#import csv
import gc
import os 


def main():
    n=int(input("Number of players to start with:"))
    F=int(input("F (payment that allows a player to go to heaven):"))
    Q=int(input("Q (fine imposed on hell-bound players):"))
    K=int(input("K (first K players go to hell):"))
    T=int(input("T (players that survive T iterations go to heaven):"))
    p=float(input("integer p between 0 and 999 (each player forgets to play with probability p/1000):"))
    title=[]
    header=['game_time','agent_position','agent_time_spent','agent_strategy','agent_probability_of_ignorance','agent_payment']
    for k in range(F+1):
        str="n_{}".format(k)+"_prop"
        title.append(str)
    game=Game(n,F,Q,T,K,p)
    # add the counts to a new row
    rows = []
    zeropayment=0
    for i in range(10000):
        print(i,'\t',len(game.agents))
        strategy = [agent.strategy for agent in game.agents]
        M=len(game.agents)-5
        extras = game.agents[-M:]
        first5 = game.agents[:5]
        payment5 = [agent.payment for agent in first5]
        time5 = [agent.time for agent in first5]
        row={}
        for j in range(F+1):
            str="n_{}".format(j)
            row[str]=strategy.count(j)
            row[str+"_prop"]=strategy.count(j)*100/len(strategy)
            #s+=strategy.count(j)
        row['game_size']=len(strategy) 
        row['mean_payment_of_first_5']=np.mean(payment5)
        row['mean_time_of_first_5']=np.mean(time5)
        collected, out=game.run()
        if out:
            paymentout = [agent.payment for agent in out]
            zeropayment+=paymentout.count(0)
            timeout = [agent.time for agent in out]
            if i>0:
                ratioout = [agent.payment/agent.time for agent in out]
                row['mean_ratio']=np.mean(ratioout)
            row['mean_payment_of_exiters']=np.mean(paymentout)
            row['mean_time_of_exiters']=np.mean(timeout)
            row['number_of_exiters']=len(out)
        row['money collected']=collected
        rows.append(row)
    print('Total money collected:', collected)
    print('Average money collected:', collected/10000)
    print('Average number of sinners who go to heaven without paying anything:', zeropayment/10000)
    pignore=game.prob/1000.0
    tit="Probability of ignorance = {}".format(pignore)
    df = pd.DataFrame(rows)
    str="game.csv"
    df.to_csv(str)
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(1.*i/(len(title)-1)) for i in range(len(title))]
    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=0,vmax=F))
    sm._A = [] 
    fig = df.plot(title=tit, y=title,color=colors,logx=True,kind='area',legend=False)
    plt.colorbar(sm)
    strpdf="./game_strategies.png"
    fig.figure.savefig(strpdf,bbox_inches='tight')
    fig1 = df.plot(title=tit, y=["game_size"],grid=True,figsize=(12.8,4.8))
    fig1.axhline(df["game_size"].mean(),c='r')
    strpdf1="./game_size.png"
    fig1.figure.savefig(strpdf1)
    fig2 = df.plot(title=tit, y=["mean_payment_of_first_5","mean_time_of_first_5"],logx=True)
    strpdf2="./game_first_5.png"
    fig2.figure.savefig(strpdf2)
    fig3 = df.plot(title=tit, y=["mean_ratio"],logx=True)
    strpdf3="./game_agentratio.png"
    fig3.figure.savefig(strpdf3)
    fig4 = df.plot(title=tit, y=["number_of_exiters","mean_time_of_exiters"],grid=True,figsize=(12.8,4.8))
    strpdf4="./game_exitersstat.png"
    fig4.figure.savefig(strpdf4)
    fig5 = df.plot(title=tit, y=["mean_payment_of_exiters"],logx=True)
    strpdf5="./game_exiterspayment.png"
    fig5.figure.savefig(strpdf5)
    fig6 = df.plot(title=tit, y=["money collected"])
    strpdf5="money_collected.png"
    fig6.figure.savefig(strpdf5)
    #fig1.close()
    plt.close('all')
    del df,row,rows
    gc.collect()

        

if __name__ == "__main__":
    main()
