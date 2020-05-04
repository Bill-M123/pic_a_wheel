import matplotlib.pyplot as plt

def make_bankroll_plot(players,bankrolls):
    guys=list(zip(players,bankrolls))
    guys.sort(key=lambda tup: tup[1], reverse=True)

    xs=[g[0] for g in guys]
    winners=[(g[0],g[1]-500) if g[1]>=500.0 else (g[0],0) for g in guys ]
    losers=[(g[0],g[1]-500) if g[1]<500.0 else (g[0],0) for g in guys]

    plt.figure(figsize=(4,3),dpi=100)
    plt.bar(xs,[w[1] for w in winners],color='darkgreen')
    plt.bar(xs,[l[1] for l in losers],color='darkred')
    plt.title('Current Winnings')
    plt.ylim(-250,250)
    plt.xticks(rotation=15)
    plt.savefig('win_lose.png')
    plt.show()
    return



players=['JohnAlba','Bornstein','Clyde','Mercer','Ed','Tardie']
bankrolls=[485,515,530,495,460,510]

make_bankroll_plot(players,bankrolls)
