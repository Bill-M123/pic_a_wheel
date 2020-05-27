# Evaluate hands for showdown

## in dealer
def evaluate_hands_calc_winnings(players):
    declared_high,declared_low = dealer.get_high_low_hands(players)
    high_hand_df, trash_high = dealer.evaluate_all_hands(declared_high)
    trash_low, low_hand_df = dealer.evaluate_all_hands(declared_low)

    # Check for everyone going the same way:
    try:
        name_check = high_hand_df['Name'][0]
    except:
        name_check='No One'

    if name_check == 'No One':
        print("high side found no one.")
        dealer.low_pot += dealer.high_pot
        dealer.high_pot = 0

    name_check='No One'
    try:
        name_check = low_hand_df['Name'][0]
    except:
        name_check='No One'
    if name_check == 'No One':
        print("low side found no one.")
        dealer.high_pot += dealer.low_pot
        dealer.low_pot = 0

    if not dealer.done_scoring:
    ###########

        high_hand_df = dealer.calc_winnings(high_hand_df, dealer.high_pot)
        low_hand_df = dealer.calc_winnings(low_hand_df, dealer.low_pot)

        dealer.high_hand_df = high_hand_df #Save for later
        dealer.low_hand_df = low_hand_df #Save for later

        # Make round and nightly scores
        dealer.make_pandl_df(players, high_hand_df, low_hand_df)
        dealer.make_summary_plots_no_pyplot(players)

        dealer.done_scoring = True
        dealer.total_player_bankroll = 0


    rolling_df = dealer.player_funds_df[['Name','In_Pot','Total_Bets','Total_Winnings','p_and_l']]
    rolling_df = rolling_df.sort_values('p_and_l', ascending=False)
    rolling_df.rename(columns={"Total_Bets": "Ante/Bet", "Total_Winnings": "Winnings", "p_and_l": "Profit"}, inplace=True)
    rolling_df = rolling_df[["Name","Ante/Bet", "Winnings", "Profit"]]
    print('rolling_df\n', rolling_df)

    #### Total_funds_check
    dealer.total_player_bankroll=rolling_df['Profit'].sum()+500*len(players)
    if (dealer.total_player_bankroll % dealer.initial_player_funds == 0):
        dealer.total_funds_check =True
    else:
        dealer.total_funds_check = False
    ####

    dealer.adjust_hi_lo_show_down_displays()
    dealer.active_player = "No one"

    dealer.calculate_bankrolls(players)
    return render_template('table_showdown.html', dealer=dealer,
                           players=new_players,high_hand_df=dealer.high_hand_df_dis,
                           low_hand_df=dealer.low_hand_df_dis,rolling_df=rolling_df)
