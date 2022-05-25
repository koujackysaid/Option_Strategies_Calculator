#!/usr/bin/env python
# coding: utf-8

# ## Option Strategies Calculator
# - cash outflow(option price, commission, loss) is denoted as negative, cash inflow(option premium, profit) as positive 
# - so when input, it should be a negative number if necessary
# - to make the formula easier to read, I tried to keep them as same as poosible, for condition the options losing value with time the standard formula with -1
# 
# remarks:
# - expected spot means you are expecting a future volatility. You can access the feasibility by comparing the required volatility for the option to be ITM with the underlying assets's volatlity distribution

# ### Long Call Option

# In[ ]:


def long_call(kc, call_option_price, 
              current_spot, expected_spot, 
              commission, number_of_call_option_contracts, shares_per_contract):
    
    # Step 1
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_call_option_contracts*shares_per_contract)
    
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    
    print('exposure_call_option:', exposure_call_option)
    
    # Cal the cost of leg A(negative number)
    upfront_cost = (call_option_price*shares_exposure_call_option)
 
    
    # Net Debit (cost for 1 unit options)
    net_debit = (call_option_price*number_of_call_option_contracts) + commission
     
    # Total Debit
    total_debit = net_debit*shares_per_contract
    
    # breakeven
    breakeven = kc + (call_option_price + commission)*-1
    print('breakeven:', breakeven)

    # Step 2
    # reward risk ratio
    if (expected_spot > kc):
        max_gain = (expected_spot - kc)*shares_exposure_call_option + total_debit
    else:
        max_gain = 0
                         
    max_drawdown = total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))
    
    # Step 3
    # cal the P&L
    if (expected_spot > kc):
        profit_from_options = (expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_options
    else:
        profit_from_options = 0
        total_profit = profit_from_options
        
    print('profit_from_options:', profit_from_options)
    
    
    # Step 4
    required_upside_volatility_percentage = (kc/current_spot - 1)*100
   
    print('required_upside_volatility_percentage:', '{:.2f}%'.format(required_upside_volatility_percentage))


# In[ ]:


long_call(50, -2, 50, 55, 0, 1, 100)


# ### Long Put Option

# In[ ]:


def long_put(kp, put_option_price, 
              current_spot, expected_spot, 
              commission, number_of_put_option_contracts, shares_per_contract):
    
    # Step 1
    # shares exposure brought by put option
    shares_exposure_put_option = (number_of_put_option_contracts*shares_per_contract)
    
    # dollar exposure brought by put option
    exposure_put_option = shares_exposure_put_option*kp
    
    print('exposure_put_option:', exposure_put_option)
    
    # Cal the cost of leg A(negative number)
    upfront_cost = (put_option_price*shares_exposure_put_option)
 
    
    # Net Debit (cost for 1 unit options)
    net_debit = (put_option_price*number_of_put_option_contracts) + commission
     
    # Total Debit
    total_debit = net_debit*shares_per_contract
    
    # breakeven
    breakeven = kp - (put_option_price + commission)*-1
    print('breakeven:', breakeven)

    # Step 2
    # reward risk ratio
    if (expected_spot < kp):
        max_gain = (kp - expected_spot)*shares_exposure_put_option + total_debit
    else:
        max_gain = 0
                         
    max_drawdown = total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))
    
    # Step 3
    # cal the P&L
    if (expected_spot < kp):
        profit_from_options = (kp - expected_spot)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_options
    else:
        profit_from_options = 0
        total_profit = profit_from_options
        
    print('profit_from_options:', profit_from_options)
    
    
    # Step 4
    required_upside_volatility_percentage = (kp/current_spot - 1)*100
   
    print('required_upside_volatility_percentage:', '{:.2f}%'.format(required_upside_volatility_percentage))


# In[ ]:


long_put(50, -2, 50, 47, 0, 1, 100)


# In[ ]:


# can use for function to review impact on risk_reward by different variables
import numpy as np
a = np.arange(46,50)
for x in a:
    print('\nK=', x)
    long_put(x,  -2, 50, 47, 0, 1, 100)


# ### Short Covered Call Option

# In[ ]:


def short_covered_call(entry_price, current_shares,
                              kc, call_option_price, 
                              current_spot, expected_spot, 
                              commission,
                              number_of_call_option_contracts,shares_per_contract):
    # Step 1
    
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_call_option_contracts*shares_per_contract)
   
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_call_option:', exposure_call_option)

    # Cal the premium (premium for 1 unit options)
    upfront_premium = call_option_price
    
    # Net premium
    net_premium = (call_option_price*number_of_call_option_contracts) + commission
   
    # Total Premium
    total_premium = net_premium*shares_per_contract
    
    # New Breakeven (the more credit, the higher for put options)
    new_breakeven = entry_price - net_premium
    print('net_premium:', net_premium)
    print('total_premium:', total_premium)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # reward risk ratio
    
    # Max gain and loss
    # option gain + stock gain + debit
    # remark : if the if statement isnt complete, liked ended with else, it could not generate a value for max_gain
    # then will have error, assigned before defined
    if (expected_spot <= kc):
        max_gain =  (expected_spot - entry_price)*current_shares + total_premium
    else:
        max_gain =  (expected_spot - entry_price)*current_shares + total_premium + (kc - expected_spot)*shares_exposure_call_option
            
                 
    max_drawdown = 1
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio (Pure Credit):', '{:.2f}%'.format(reward_risk_ratio))
    
    # Step 3
    # cal the P&L
    
    if (expected_spot <= kc):
        new_shares_holding = current_shares
        # profit from stock (positive number):
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff (negative number)
        profit_from_options = total_premium
        # Total profit
        total_profit = profit_from_stock + profit_from_options
    else:
        new_shares_holding = current_shares
        # profit from stock (positive number):
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff (negative number)
        profit_from_options = total_premium + (kc - expected_spot)*shares_exposure_call_option
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        
    print('new_shares_holding(unchanged as):', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)

    # Step 4
    required_upside_volatility_percentage = (kc/current_spot - 1)*100
   
    print('required_upside_volatility_percentage:', '{:.2f}%'.format(required_upside_volatility_percentage))


# In[ ]:


short_covered_call(80, 100, 90, 2, 85, 88, 0, 1, 100)


# In[ ]:


import numpy as np
a = np.arange(85,100,5)
for x in a:
    print('\nexpected_spot=', x)
    short_covered_call(80, 100, 90, 2, 85, x, 0, 1, 100)


# ### Short Covered Call Collar Option

# In[ ]:


def short_covered_call_collar(entry_price, current_shares,
                              kc, call_option_price, 
                              kp, put_option_price,
                              current_spot, expected_spot, 
                              commission,
                              number_of_call_option_contracts, number_of_put_option_contracts,
                              shares_per_contract):
    # Step 1
    
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_put_option_contracts*shares_per_contract)
    
    # shares exposure brought by put option
    shares_exposure_put_option = (number_of_call_option_contracts*shares_per_contract)
   
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    
    # dollar exposure brought by put option
    exposure_put_option = shares_exposure_call_option*kp
    
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_call_option:', exposure_call_option)
    print('exposure_put_option:', exposure_put_option)

    # Cal the premium of leg A(premium for 1 unit options)
    upfront_premium = call_option_price
    
    # Cal the cost of leg B
    upfront_cost = put_option_price
    
    # Net premium (a negative number when it is debit)
    net_premium = (put_option_price*number_of_put_option_contracts) + (call_option_price*number_of_call_option_contracts) + commission
     
    # Total premium
    total_premium = net_premium*shares_per_contract
    
    
    # New Breakeven (the more credit, the higher for put options)
    new_breakeven = entry_price - net_premium
    print('net_premium:', net_premium)
    print('total_premium:', total_premium)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # reward risk ratio
    
    # Max gain and loss
    # option gain + stock gain + debit/premium
    # remark : if the if statement isnt complete, liked ended with else, it could not generate a value for max_gain
    # then will have error, assigned before defined
    if (expected_spot > kc):
        max_gain = -1*(expected_spot - kc)*shares_exposure_call_option + (expected_spot - entry_price)*current_shares + total_premium 
    elif (expected_spot<=kc) and (expected_spot > entry_price):
        max_gain = (expected_spot - entry_price)*current_shares + total_premium
    elif (expected_spot<entry_price) and (expected_spot >= kp):
        max_gain = (expected_spot - entry_price)*current_shares + total_premium
    else:
        max_gain = (expected_spot - entry_price)*current_shares + total_premium + (kp - expected_spot)*shares_exposure_put_option
                     
    max_drawdown = (expected_spot - kp)*current_shares + total_premium
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio (Pure Credit):', '{:.2f}%'.format(reward_risk_ratio))
    
    # Step 3
    # cal the P&L

    if (expected_spot > kc):
        new_shares_holding = current_shares
        # profit from stock (positive number):
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # loss from options payoff
        profit_from_options = -1*(expected_spot - kc)*shares_exposure_call_option + total_premium
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 1')
        
    elif (expected_spot<=kc) and (expected_spot > kp):
        new_shares_holding = current_shares
        # profit from stock (positive number):
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # loss from options payoff
        profit_from_options = total_premium
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 2')
    
    else:
        new_shares_holding = current_shares
        # profit from stock (positive number):
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff 
        profit_from_options = total_premium + (kp - expected_spot)*shares_exposure_put_option
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 3')
        
    print('new_shares_holding(unchanged as):', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)

    # Step 4
    required_upside_volatility_percentage = (kc/current_spot - 1)*100
    required_downside_volatility_percentage = (kp/current_spot - 1)*100
   
    print('required_upside_volatility_percentage:', '{:.2f}%'.format(required_upside_volatility_percentage))
    print('required_downside_volatility_percentage:', '{:.2f}%'.format(required_downside_volatility_percentage))


# In[ ]:


short_covered_call_collar(80, 100,
                              110, 3, 
                              70, -2,
                              90, 120, 
                              0,
                              1,1,
                              100)


# In[ ]:


import numpy as np
a = np.arange(70,125, 5)
for x in a:
    print('\nexpected_spot=', x)
    short_covered_call_collar(80, 100,
                              110, 3, 
                              70, -2,
                              90, x, 
                              0,
                              1,1,
                              100)


# ### Bull Call Spread Option

# In[ ]:


def bull_call_spread(entry_price, current_shares,
                              kc, call_option_price, 
                              kc1, further_call_option_price,
                              current_spot, expected_spot, 
                              commission, number_of_call_option_contracts, number_of_further_call_option_contracts,
                              shares_per_contract):
    # Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_call_option_contracts*shares_per_contract)
    # shares exposure brought by further call option
    shares_exposure_further_call_option = (number_of_further_call_option_contracts*shares_per_contract)
    
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    # dollar exposure brought by further call option
    exposure_further_call_option = shares_exposure_further_call_option*kc1
   
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_call_option:', exposure_call_option)
    print('exposure_further_call_option:', exposure_further_call_option)

    
    # Cal the cost of leg A
    upfront_cost = call_option_price
    # Cal the premium of leg B
    upfront_premium = further_call_option_price
    
    # Net Debit
    net_debit = (call_option_price*number_of_call_option_contracts) + (further_call_option_price*number_of_further_call_option_contracts) + commission
    # Total Debit
    total_debit = net_debit*shares_per_contract
    
    # New Breakeven
    if entry_price != 0:
        new_breakeven = entry_price + -1*net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # reward risk ratio
    # Max gain and loss
    # option gain + stock gain + debit
    max_gain = (kc1 - kc)*shares_exposure_call_option +(kc1 - entry_price)*current_shares + total_debit
    max_drawdown = (expected_spot - entry_price)*current_shares + total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))

    # Step 3
    # cal the P&L

    if (expected_spot>entry_price) and (expected_spot<kc) :
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
    
    elif (expected_spot>kc) and (expected_spot<=kc1):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        
    elif expected_spot>kc1:
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (kc1 - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options

    else:
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = total_debit
        # Total loss
        total_loss = profit_from_stock + profit_from_options
    print('new_shares_holding:', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
    # Step 4
    required_upside_volatility_to_kc_percentage = (kc/current_spot - 1)*100
    required_upside_volatility_to_kc1_percentage = (kc1/current_spot - 1)*100
   
    print('required_upside_volatility_to_kc_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc_percentage))
    print('required_upside_volatility_to_kc1_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc1_percentage))


# In[ ]:


bull_call_spread(0, 0,
                100, -3,
                120, 1,
                80, 130,
                0, 1, 1, 100)


# In[ ]:


import numpy as np
a = np.arange(90,130,10)
for x in a:
    print('\nexpected_spot=', x)
    bull_call_spread(0, 0,
                100, -3,
                120, 1,
                80, x,
                0, 1, 1, 100)


# ### Bear Put Spread Option

# In[ ]:


def bear_put_spread(entry_price, current_shares,
                              kp, put_option_price, 
                              kp1, further_put_option_price,
                              current_spot, expected_spot, 
                              commission, number_of_put_option_contracts, number_of_further_put_option_contracts,
                              shares_per_contract):
    # Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by put option
    shares_exposure_put_option = (number_of_put_option_contracts*shares_per_contract)
    # shares exposure brought by further put option
    shares_exposure_further_put_option = (number_of_further_put_option_contracts*shares_per_contract)
    
    # dollar exposure brought by put option
    exposure_put_option = shares_exposure_put_option*kp
    # dollar exposure brought by further put option
    exposure_further_put_option = shares_exposure_further_put_option*kp1
   
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_put_option:', exposure_put_option)
    print('exposure_further_put_option:', exposure_further_put_option)

    
    # Cal the cost of leg A
    upfront_cost = put_option_price
    # Cal the premium of leg B
    upfront_premium = further_put_option_price
    
    # Net Debit
    net_debit = (put_option_price*number_of_put_option_contracts) + (further_put_option_price*number_of_further_put_option_contracts) + commission
    # Total Debit
    total_debit = net_debit*shares_per_contract
    
    # New Breakeven
    if entry_price != 0:
        new_breakeven = entry_price + net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # reward risk ratio
    # Max gain and loss
    # option gain + stock gain + debit
    max_gain = -1*(kp1 - kp)*shares_exposure_put_option + -1*(kp1 - entry_price)*current_shares + total_debit
    max_drawdown = -1*(expected_spot - entry_price)*current_shares + total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))

    # Step 3
    # cal the P&L

    if (expected_spot<entry_price) and (expected_spot>kp) :
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = -1*(expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
    
    elif (expected_spot<kp) and (expected_spot>=kp1):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = -1*(expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = -1*(expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        
    elif expected_spot<kp1:
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = -1*(expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = -1*(kp1 - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
    
    else:
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = -1*(expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = total_debit
        # Total loss
        total_loss = profit_from_stock + profit_from_options
    print('new_shares_holding:', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
    # Step 4
    required_upside_volatility_to_kp_percentage = (kp/current_spot - 1)*100
    required_upside_volatility_to_kp1_percentage = (kp1/current_spot - 1)*100
   
    print('required_upside_volatility_to_kp_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kp_percentage))
    print('required_upside_volatility_to_kp1_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kp1_percentage))


# In[ ]:


bear_put_spread(0,0 ,
                80, -3,
                60, 1,
                100, 60,
                0, 1,1,100) 


# In[ ]:


import numpy as np
# rmb from bigger to smaller, we use -5, not 5, otherwise cannot run the code
a = np.arange(90,40,-10)
for x in a:
    print('\nexpected_spot=', x)
    bear_put_spread(0,0 ,
                80, -3,
                60, 1,
                100, x,
                0, 1,1,100)


# ### Short Bull Ratio Spread Option
# - assume no stock position is holding, so max loss is debit + loss from SC

# In[ ]:


def short_bull_ratio_spread(entry_price, current_shares,
                              kc, call_option_price, 
                              kc1, further_call_option_price,
                              current_spot, expected_spot, 
                              commission,
                              number_of_call_option_contracts, number_of_further_call_option_contracts,
                              shares_per_contract):

    # Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_call_option_contracts*shares_per_contract)
    # shares exposure brought by further call option
    shares_exposure_further_call_option = (number_of_further_call_option_contracts*shares_per_contract)
    
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    # dollar exposure brought by further call option
    exposure_further_call_option = shares_exposure_further_call_option*kc1
   
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_call_option:', exposure_call_option)
    print('exposure_further_call_option:', exposure_further_call_option)


    # Cal the cost of leg A
    upfront_cost = further_call_option_price*(number_of_further_call_option_contracts)
    # Cal the premium of leg B
    upfront_premium = call_option_price*(number_of_call_option_contracts)
    
    # Net Debit
    net_debit = upfront_cost + upfront_premium + commission
    # total_debit
    total_debit = net_debit*shares_per_contract
    
    # New Breakeven
    if entry_price != 0:
        new_breakeven = entry_price + -1*net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # Max gain and loss (assume no stock holding)
    # option gain + stock gain + debit
    
    if (expected_spot > kc1):
        max_gain = (expected_spot - kc1)*shares_exposure_further_call_option 
        + (-1)*(kc1 - kc)*shares_exposure_call_option + total_debit
    
    else:
        max_gain = 0
    
    max_drawdown = -1*(kc1 - kc)*(shares_exposure_call_option) + total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', reward_risk_ratio)
    
    # Step 3
    # cal the P&L

    if (expected_spot > kc1):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (expected_spot - kc1)*shares_exposure_further_call_option + -1*(expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 1')
       
    
    elif (expected_spot<=kc1) and (expected_spot >kc):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # loss from options payoff(need the loss the be negative here)
        profit_from_options = -1*(expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 2')
       
    else:
        new_shares_holding = current_shares
        # loss from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # loss from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 3')
    
    print('new_shares_holding:', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
    # Step 4 (no need kc here, since already ITM)
    required_upside_volatility_to_kc1_percentage = (kc1/current_spot - 1)*100
   

    print('required_upside_volatility_to_kc1_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc1_percentage))


# In[ ]:


short_bull_ratio_spread(0,0,
                       10, 3.65,
                       15, -1.35,
                       12.54, 10,
                       0,
                       6, 18,
                       100)


# In[ ]:


import numpy as np
# rmb from bigger to smaller, we use -5, not 5, otherwise cannot run the code
a = np.arange(5, 25, 5)
for x in a:
    print('\nexpected_spot=', x)
    short_bull_ratio_spread(0,0,
                       10, 3.65,
                       15, -1.35,
                       12.54, x,
                       0,
                       6, 18,
                       100)


# ### Short Bear Ratio Spread Option
# - assume no stock position is holding, so max loss is debit + loss from SP

# In[ ]:


def short_bear_ratio_spread(entry_price, current_shares,
                              kp, put_option_price, 
                              kp1, further_put_option_price,
                              current_spot, expected_spot, 
                              commission,
                              number_of_put_option_contracts, number_of_further_put_option_contracts,
                              shares_per_contract):

    # Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by put option
    shares_exposure_put_option = (number_of_put_option_contracts*shares_per_contract)
    # shares exposure brought by further put option
    shares_exposure_further_put_option = (number_of_further_put_option_contracts*shares_per_contract)
    
    # dollar exposure brought by put option
    exposure_put_option = shares_exposure_put_option*kp
    # dollar exposure brought by further put option
    exposure_further_put_option = shares_exposure_further_put_option*kp1
   
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_put_option:', exposure_put_option)
    print('exposure_further_put_option:', exposure_further_put_option)


    # Cal the cost of leg A
    upfront_cost = further_put_option_price*(number_of_further_put_option_contracts)
    # Cal the premium of leg B
    upfront_premium = put_option_price*(number_of_put_option_contracts)
    
    # Net Debit
    net_debit = upfront_cost + upfront_premium + commission
    # total_debit
    total_debit = net_debit*shares_per_contract
    
    # New Breakeven
    if entry_price != 0:
        new_breakeven = entry_price + net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    
    # Step 2
    # Max gain and loss (assume no stock holding)
    # option gain + stock gain + debit
    
    if (expected_spot < kp1):
        max_gain = -1*(expected_spot - kp1)*shares_exposure_further_put_option 
        + (kp1 - kp)*shares_exposure_put_option + total_debit
    
    else:
        max_gain = 0
    
    max_drawdown = (kp1 - kp)*(shares_exposure_put_option) + total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', reward_risk_ratio)
    
    # Step 3
    # cal the P&L

    if (expected_spot < kp1):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = -1*(expected_spot - kp1)*shares_exposure_further_put_option 
        + (expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 1')
       
    
    elif (expected_spot>=kp1) and (expected_spot < kp):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # loss from options payoff(need the loss the be negative here)
        profit_from_options = (expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 2')
       
    else:
        new_shares_holding = current_shares
        # loss from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # loss from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 3')
    
    print('new_shares_holding:', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
    # Step 4 (no need kp here, since already ITM)
    required_upside_volatility_to_kp1_percentage = (kp1/current_spot - 1)*100
   

    print('required_upside_volatility_to_kp1_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kp1_percentage))


# In[ ]:


short_bear_ratio_spread(0,0,
                        35,6,
                        28,-1.5,
                        37,20,
                        0,
                        3,12,
                        100
)


# In[ ]:


import numpy as np
# rmb from bigger to smaller, we use -5, not 5, otherwise cannot run the code
a = np.arange(40, 20, -5)
for x in a:
    print('\nexpected_spot=', x)
    short_bear_ratio_spread(0,0,
                        35,6,
                        28,-1.5,
                        37,x,
                        0,
                        3,12,
                        100
)


# ### Bull Call Ladder Spread Option

# In[ ]:


def bull_call_spread(entry_price, current_shares,
                              kc, call_option_price, 
                              kc1, further_call_option_price,
                              kc2, more_further_call_option_price,
                              current_spot, expected_spot, 
                              commission,
                              number_of_call_option_contracts, number_of_further_call_option_contracts,
                              number_of_more_further_call_option_contracts,
                              shares_per_contract):

    # Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_call_option_contracts*shares_per_contract)
    # shares exposure brought by further call option
    shares_exposure_further_call_option = (number_of_further_call_option_contracts*shares_per_contract)
    # shares exposure brought by more further call option
    shares_exposure_more_further_call_option = (number_of_more_further_call_option_contracts*shares_per_contract)
    
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    # dollar exposure brought by further call option
    exposure_further_call_option = shares_exposure_further_call_option*kc1
    # dollar exposure brought by more further call option
    exposure_more_further_call_option = shares_exposure_more_further_call_option*kc2
    
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_call_option:', exposure_call_option)
    print('exposure_further_call_option:', exposure_further_call_option)
    print('exposure_more_further_call_option:', exposure_more_further_call_option)

    # Cal the cost of leg A
    upfront_cost = call_option_price*number_of_call_option_contracts
    # Cal the premium of leg B
    upfront_premium = (further_call_option_price*number_of_further_call_option_contracts) + (more_further_call_option_price*number_of_more_further_call_option_contracts)
    
    # Net Debit (a negative number when it is debit, assumed input of commission is a positive)
    net_debit = upfront_cost + upfront_premium
    # Total Debit
    total_debit = net_debit*shares_per_contract
    # New Breakeven
    if entry_price != 0:
        new_breakeven = entry_price - -1*net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # Max gain and loss
    # option gain + stock gain + debit
    max_gain = (kc1 - kc)*shares_exposure_call_option +(expected_spot - entry_price)*current_shares + total_debit
    
    if (expected_spot>kc1) and (expected_spot<kc2):
        max_drawdown = -1*(expected_spot - kc1)*shares_exposure_further_call_option + (expected_spot - kc)*shares_exposure_call_option + (expected_spot - entry_price)*current_shares + total_debit
    elif expected_spot>kc2:
        max_drawdown = -1*(expected_spot - kc2)*shares_exposure_more_further_call_option + -1*(expected_spot - kc1)*shares_exposure_further_call_option + (expected_spot - kc)*shares_exposure_call_option + (expected_spot - entry_price)*current_shares + total_debit
    else:
        max_drawdown = total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))

    # Step 3
    # cal the P&L

    if (expected_spot<kc) :
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 1')
    
    elif (expected_spot>kc) and (expected_spot<=kc1):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 2')
        
    elif (expected_spot>kc1) and (expected_spot<=kc2):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = -1*(expected_spot - kc1)*shares_exposure_further_call_option + (expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 3')
        
    else:
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (-1*(expected_spot - kc2)*shares_exposure_more_further_call_option) + -1*(kc1 - expected_spot)*shares_exposure_further_call_option + (expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 4')
    
    print('new_shares_holding:', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
    # Step 4
    required_upside_volatility_to_kc_percentage = (kc/current_spot - 1)*100
    required_upside_volatility_to_kc1_percentage = (kc1/current_spot - 1)*100
    required_upside_volatility_to_kc2_percentage = (kc2/current_spot - 1)*100

    print('required_upside_volatility_to_kc_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc_percentage))
    print('required_upside_volatility_to_kc1_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc1_percentage))
    print('required_upside_volatility_to_kc2_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc2_percentage))


# In[ ]:


bull_call_spread(0,0,
                 220,-7.6,
                 235,2.7,
                 240,1.8,
                 218, 240,
                 0,
                 1,1,1,
                 100                 
)
# remarks: profit when x=235, and x =240 is the same
# (235-220) = 15
# (235-240) + (240-220) = 15


# In[ ]:


import numpy as np
# rmb from bigger to smaller, we use -5, not 5, otherwise cannot run the code
a = np.arange(215,250,5)
for x in a:
    print('\nexpected_spot=', x)
    bull_call_spread(0,0,
                 220,-7.6,
                 235,2.7,
                 240,1.8,
                 218, x,
                 0,
                 1,1,1,
                 100                 
)


# ### Bear Put Ladder Spread Option

# In[ ]:


def bear_put_spread(entry_price, current_shares,
                              kp, put_option_price, 
                              kp1, further_put_option_price,
                              kp2, more_further_put_option_price,
                              current_spot, expected_spot, 
                              commission,
                              number_of_put_option_contracts, number_of_further_put_option_contracts,
                              number_of_more_further_put_option_contracts,
                              shares_per_contract):

# Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by put option
    shares_exposure_put_option = (number_of_put_option_contracts*shares_per_contract)
    # shares exposure brought by further put option
    shares_exposure_further_put_option = (number_of_further_put_option_contracts*shares_per_contract)
    # shares exposure brought by more further put option
    shares_exposure_more_further_put_option = (number_of_more_further_put_option_contracts*shares_per_contract)
    
    # dollar exposure brought by put option
    exposure_put_option = shares_exposure_put_option*kp
    # dollar exposure brought by further put option
    exposure_further_put_option = shares_exposure_further_put_option*kp1
    # dollar exposure brought by more further put option
    exposure_more_further_put_option = shares_exposure_more_further_put_option*kp2
    
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_put_option:', exposure_put_option)
    print('exposure_further_put_option:', exposure_further_put_option)
    print('exposure_more_further_put_option:', exposure_more_further_put_option)

    # Cal the cost of leg A
    upfront_cost = put_option_price*number_of_put_option_contracts
    # Cal the premium of leg B
    upfront_premium = (further_put_option_price*number_of_further_put_option_contracts) + (more_further_put_option_price*number_of_more_further_put_option_contracts)
    
    # Net Debit (a negative number when it is debit, assumed input of commission is a positive)
    net_debit = upfront_cost + upfront_premium
    # Total Debit
    total_debit = net_debit*shares_per_contract
    # New Breakeven
    if entry_price != 0:
        new_breakeven = entry_price + net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # Max gain and loss
    # option gain + stock gain + debit
    max_gain = (kp - kp1)*shares_exposure_put_option +(entry_price - kp1)*current_shares + total_debit
    
    if (expected_spot<kp1) and (expected_spot>=kp2):
        max_drawdown = (expected_spot - kp1)*shares_exposure_further_put_option + -1*(expected_spot - kp)*shares_exposure_put_option + (expected_spot - entry_price)*current_shares + total_debit
    elif expected_spot<kp2:
        max_drawdown = (expected_spot - kp2)*shares_exposure_more_further_put_option + (expected_spot - kp1)*shares_exposure_further_put_option + (expected_spot - kp)*shares_exposure_put_option + (expected_spot - entry_price)*current_shares + total_debit
    else:
        max_drawdown = total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))

    # Step 3
    # cal the P&L

    if (expected_spot>kp) :
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 1')
    
    elif (expected_spot<kp) and (expected_spot>=kp1):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = -1*(expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 2')
        
    elif (expected_spot<kp1) and (expected_spot>=kp2):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (expected_spot - kp1)*shares_exposure_further_put_option + -1*(expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 3')
        
    else:
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = ((expected_spot - kp2)*shares_exposure_more_further_put_option) + (expected_spot - kp1)*shares_exposure_further_put_option + -1*(expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 4')
    
    print('new_shares_holding:', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
    # Step 4
    required_upside_volatility_to_kp_percentage = (kp/current_spot - 1)*100
    required_upside_volatility_to_kp1_percentage = (kp1/current_spot - 1)*100
    required_upside_volatility_to_kp2_percentage = (kp2/current_spot - 1)*100

    print('required_upside_volatility_to_kp_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kp_percentage))
    print('required_upside_volatility_to_kp1_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kp1_percentage))
    print('required_upside_volatility_to_kp2_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kp2_percentage))


# In[ ]:


bear_put_spread(0,0,
                 92.5,-4.35,
                 80,0.88,
                 75,0.46,
                 93, 70,
                 0,
                 2,2,2,
                 100)             


# In[ ]:


import numpy as np
# rmb from bigger to smaller, we use -5, not 5, otherwise cannot run the code
a = np.arange(95,55,-5)
for x in a:
    print('\nexpected_spot=', x)
    bear_put_spread(0,0,
                 92.5,-4.35,
                 80,0.88,
                 75,0.46,
                 93, x,
                 0,
                 2,2,2,
                 100)     


# ### Long Straddle Option
# - Long Strangle is using OTM with the same mechanism, ratio of call and put is 1:1
# - Strap Straddle is call options with bigger ratio, can be from 2:1 to any
# - Strip Straddle is put options with bigger ratio, can be from 2:1 to any
# - both can use this calculator

# In[ ]:


def Long_Straddle(entry_price, current_shares,
                              kc, call_option_price, 
                              kp, put_option_price,
                              current_spot, expected_spot, 
                              commission,
                              number_of_call_option_contracts, number_of_put_option_contracts,
                              shares_per_contract):
    # Step 1
    #initial exposure
    initial_exposure = entry_price*current_shares
    # current exposure
    current_exposure = current_spot*current_shares
    
    # shares exposure brought by call option
    shares_exposure_call_option = (number_of_call_option_contracts*shares_per_contract)
    # shares exposure brought by put option
    shares_exposure_put_option = (number_of_put_option_contracts*shares_per_contract)
   
    
    # dollar exposure brought by call option
    exposure_call_option = shares_exposure_call_option*kc
    # dollar exposure brought by put option
    exposure_put_option = shares_exposure_put_option*kp
    
    
    print('initial_exposure:', initial_exposure)
    print('current_exposure:', current_exposure)
    print('exposure_call_option:', exposure_call_option)
    print('exposure_put_option:', exposure_put_option)

    # Cal the cost of leg A
    upfront_cost = (call_option_price*number_of_call_option_contracts)+ (put_option_price*number_of_put_option_contracts)
    # Cal the premium of leg B, no premium in this case
    upfront_premium = 0
    
    # Net Debit (a negative number when it is debit, assumed input of commission is a positive)
    net_debit = upfront_cost + upfront_premium
     
    # Total Debit
    total_debit = net_debit*shares_per_contract
    
    # New Breakeven (the more credit, the higher for put options)
    if entry_price != 0:
        new_breakeven = entry_price + -1*net_debit
    else:
        new_breakeven = 0
    print('net_debit:', net_debit)
    print('total_debit:', total_debit)
    print('new_breakeven:', new_breakeven)

    # Step 2
    # Max gain and loss
    # option gain + stock gain + debit
    # remark : if the if statement isnt complete, liked ended with else, it could not generate a value for max_gain
    # then will have error, assigned before defined
    if (expected_spot > kc) and (expected_spot > kp):
        max_gain = (expected_spot - kc)*shares_exposure_call_option + (expected_spot - entry_price)*current_shares + total_debit
    elif (expected_spot < kc) and (expected_spot < kp):
        max_gain = -1*(expected_spot - kp)*shares_exposure_call_option + (expected_spot - entry_price)*current_shares + total_debit
    else:
        max_gain = (expected_spot - entry_price)*current_shares
        
    max_drawdown = total_debit
    
    reward_risk_ratio = abs(max_gain/max_drawdown)*100
    print('max_gain:', max_gain)
    print('max_drawdown:', max_drawdown)
    print('reward_risk_ratio:', '{:.2f}%'.format(reward_risk_ratio))

    # Step 3
    # Cal the P&L
    if (expected_spot > kc) and (expected_spot > kp):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = (expected_spot - kc)*shares_exposure_call_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 1')
    
    elif (expected_spot < kc) and (expected_spot < kp):
        new_shares_holding = current_shares
        # profit from stock:
        profit_from_stock = (expected_spot - entry_price)*current_shares
        # profit from options payoff
        profit_from_options = -1*(expected_spot - kp)*shares_exposure_put_option + total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 2')

    else:
        new_shares_holding = current_shares
        # loss from stock (negative number):
        profit_from_stock = (current_spot - entry_price)*current_shares
        # loss from options payoff
        profit_from_options = total_debit
        # Total profit
        total_profit = profit_from_stock + profit_from_options
        print('condition 3')
    
    print('new_shares_holding(unchanged as):', new_shares_holding)
    print('profit_from_stock:', profit_from_stock)
    print('profit_from_options:', profit_from_options)
    
# Step 4
    required_upside_volatility_to_kc_percentage = (kc/current_spot - 1)*100
    required_downside_volatility_to_kp_percentage = (kp/current_spot - 1)*100

    print('required_upside_volatility_to_kc_percentage:', '{:.2f}%'.format(required_upside_volatility_to_kc_percentage))
    print('required_downside_volatility_to_kp_percentage:', '{:.2f}%'.format(required_downside_volatility_to_kp_percentage))
    


# In[ ]:


Long_Straddle(0,0,
                 50,-2,
                 50,-2,
                 50,42,
                 0,
                 1,1,
                 100)   


# In[ ]:


import numpy as np
# rmb from bigger to smaller, we use -5, not 5, otherwise cannot run the code
a = np.arange(40,65,5)
for x in a:
    print('\nexpected_spot=', x)
    Long_Straddle(0,0,
                 50,2,
                 50,2,
                 50,x,
                 0,
                 1,1,
                 100)


# Strap Straddle case
# - More on call, bullish

# In[ ]:


Long_Straddle(0,0,
                 70,-3.4,
                 70,-2.15,
                 71,83,
                 0,
                 2,1,
                 100)   


# Strip Stradddle Case
# - more on put, bearish

# In[ ]:


Long_Straddle(0,0,
                 70,-3.4,
                 70,-2.15,
                 71,65,
                 0,
                 1,2,
                 100)   

