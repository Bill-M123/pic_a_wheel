# Evaluate hands for showdown

## in dealer
def evaluate_hands_calc_winnings(self,players):
    declared_high,declared_low = self.get_high_low_hands(players)
    high_hand_df, trash_high = self.evaluate_all_hands(declared_high)
    trash_low, low_hand_df = self.evaluate_all_hands(declared_low)

    # Check for everyone going the same way:
    try:
        name_check = high_hand_df['Name'][0]
    except:
        name_check='No One'

    if name_check == 'No One':
        print("high side found no one.")
        self.low_pot += self.high_pot
        self.high_pot = 0

    name_check='No One'
    try:
        name_check = low_hand_df['Name'][0]
    except:
        name_check='No One'
    if name_check == 'No One':
        print("low side found no one.")
        self.high_pot += self.low_pot
        self.low_pot = 0

    ###########

    high_hand_df = self.calc_winnings(high_hand_df, self.high_pot)
    low_hand_df = self.calc_winnings(low_hand_df, self.low_pot)

    self.high_hand_df = high_hand_df #Save for later
    self.low_hand_df = low_hand_df #Save for later

    # Make round and nightly scores
    if not self.summaries_made:
        self.make_pandl_df(players, high_hand_df, low_hand_df)
        self.make_summary_plots_no_pyplot(players)
        self.summaries_made = True

        self.total_player_bankroll = 0

        rolling_df = self.player_funds_df[['Name','In_Pot','Total_Bets','Total_Winnings','p_and_l']]
        rolling_df = rolling_df.sort_values('p_and_l', ascending=False)
        rolling_df.rename(columns={"Total_Bets": "Ante/Bet", "Total_Winnings": "Winnings", "p_and_l": "Profit"}, inplace=True)
        rolling_df = rolling_df[["Name","Ante/Bet", "Winnings", "Profit"]]
        self.rolling_df = rolling_df
        print('rolling_df\n', rolling_df)

    else:
        pass

    #### Total_funds_check
    self.total_player_bankroll=rolling_df['Profit'].sum()+500*len(players)

    if (self.total_player_bankroll % self.initial_player_funds == 0):
        self.total_funds_check =True
    else:
        self.total_funds_check = False
    ####

    self.adjust_hi_lo_show_down_displays()
    self.active_player = "No one"

    self.calculate_bankrolls(players)

    self.done_scoring = True
    self.hand_in_progress = False
    self.active_player = 'No one'
    self.showdown = True
    return
