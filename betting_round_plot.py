import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def make_hand_plot(players,hand_contributions,num_hands):
    '''Make bettinground summary plot'''
    tmp=[]
    for g,guy in enumerate(players):
        for h,hand in enumerate(hand_contributions[g]):
            tmp.append([guy,h,hand,num_hands[g][h]])
    guys_df=pd.DataFrame(columns=['Name','rnd','rnd_pot','num_hnds'],
                data=tmp)
    guys_df['rnd_ttl']=guys_df['rnd_pot']
    guys_df['cum_bet']=guys_df.groupby("Name")["rnd_ttl"].cumsum().fillna(0)
    tls=guys_df.pivot_table(index='Name',values='rnd_ttl',\
            aggfunc='sum').reset_index(drop=False).rename(columns={'rnd_ttl':'ttl'})
    guys_df=pd.merge(guys_df,tls,on='Name')
    guys_df.sort_values(["ttl","rnd"],ascending=[False,True],inplace=True)

    colors_dict={0:'red',1:'yellow',2:'darkgreen'}

    plt.figure(figsize=(5,3),dpi=100)
    for r in sorted(list(guys_df.rnd.unique())):
        tmp=guys_df.loc[guys_df.rnd==r,:]

        if r==0:
            bottoms=tmp.rnd
        else:
            tmp2=guys_df.loc[guys_df.rnd==r-1,:]
            bottoms=tmp2.cum_bet
        xs=list(tmp.Name)
        colors=[colors_dict[x] for x in tmp.num_hnds.values]
        plt.bar(range(len(xs)),tmp.rnd_ttl,bottom=bottoms,color=colors,edgecolor='gray')

    rectangle = plt.Rectangle((4,50), .25, 5, fc='darkgreen',ec="black")
    plt.gca().add_patch(rectangle)
    plt.text(4,57,"End of Round")
    plt.text(4.5,50,"Two Hands")
    rectangle = plt.Rectangle((4,45), .25, 5, fc='yellow',ec="black")
    plt.gca().add_patch(rectangle)
    plt.text(4.5,45,"One Hands")
    rectangle = plt.Rectangle((4,40), .25, 5, fc='red',ec="black")
    plt.gca().add_patch(rectangle)
    plt.text(4.5,40,"Folded")

    plt.title("How committed are they?")
    plt.xticks(np.arange(len(xs)),labels=xs,rotation=15)
    plt.tight_layout()
    plt.savefig('betting_rounds.png')
    plt.show()
    return



players=['JohnAlba','Bornstein','Clyde','Mercer','Ed','Tardie']
bankrolls=[485,515,530,495,460,510]
hand_contributions=[[10,20,20,10],[10,20,20,5],[10,20,10,5],[5,10,10,0],[5,5,0,0],
                    [0,0,0,0]]
num_hands=[[2,2,2,2],[2,2,2,1],[2,2,1,1],[1,1,0,0],[1,0,0,0],
                    [0,0,0,0]]

make_hand_plot(players,hand_contributions,num_hands)
