import pandas as pd

def get_statistics_two(team_name, team_prefix, side, stat_type, project_name=None, save_folder=None):
    
    gamelist = []
    
    teams = {
        'Steelers': ['401437634', '401437636', '401437735', '401437757', '401437763', '401437785', '401437735',
                    '401437812', '401437838', '401437856', '401437872', '401437874', '401437894', '401437907', 
                    '401437928', '401437934', '401437958'],
        'Bills': ['401437654', '401436831', '401437738', '401437750', '401437654', '401437788', '401437817',
                 '401437826', '401437833', '401437847', '401437857', '401437873', '401437889', '401437902',
                 '401437920', '401437949'],
        'Chiefs': ['401437653', '401434030', '401437638', '401437470', '401437776', '401437788', '401437802',
                  '401437830', '401437835', '401437854', '401437869', '401437884', '401437899', '401437909',
                  '401437922', '401437937', '401437961'],
        'Bengals': ['401437634', '401437734', '401437740', '401437748', '401437775', '401437783', '401437794', 
                   '401437818', '401437822', '401437856', '401437865', '401437884', '401437890', '401437914',
                   '401437924', '401437951'],
        'Browns': ['401437651', '401437635', '401437735' ,'401437749', '401437764', '401437779', '401437792',
                  '401437818', '401437836', '401437847', '401437861', '401437878', '401437890', '401437903',
                  '401437921', '401437942', '401437958'],
        'Ravens': ['401437632', '401437633', '401437631' ,'401437750', '401437775', '401437784', '401437792',
                  '401437805', '401437831', '401437846', '401437862', '401437875', '401437894', '401437903',
                  '401437918', '401437934', '401437951'],
        'FortyNiners': ['401437647', '401437605', '401437746' ,'401437761', '401437772', '401437778', '401437802',
                       '401437815', '401437842', '401435642', '401437870', '401437883', '401437897', '401437901',
                       '401437926', '401437943', '401437962']}

    gameids = teams.get(team_name, [])

    for num in gameids:
        link = f'https://www.espn.com/nfl/matchup/_/gameId/{num}'
        gamelist.append(link)  

    #in the function = change PIT to team name
    stats = pd.DataFrame()

    for link in gamelist:
        website = pd.read_html(link)
        df = website[0]
        df2 = website[1]
        rename = df2.rename(columns = {'Unnamed: 1': df.iloc[0,0], 'Unnamed: 2': df.iloc[1,0]})
        
        if side == 'offense':
            rename.drop_duplicates(subset = ['Team Stats'], inplace = True)
            stats = stats.append(rename[['Team Stats', team_prefix]])
        elif side == 'defense':
            new = rename
            new.drop(columns = [team_prefix], inplace = True)
            new.rename(columns={ new.columns[1]: team_prefix + '_' + "Opponent"}, inplace = True)
            new.drop_duplicates(subset = ['Team Stats'], inplace = True)
            stats = stats.append(new)       

    stats_name = stats[(stats['Team Stats'] != '3rd down efficiency') &
                       (stats['Team Stats'] != '4th down efficiency') &
                       (stats['Team Stats'] != '4th down efficiency') &
                       (stats['Team Stats'] != 'Comp-Att') &
                       (stats['Team Stats'] != 'Sacks-Yards Lost') &
                       (stats['Team Stats'] != 'Red Zone (Made-Att)') &
                       (stats['Team Stats'] != 'Possession') &
                       (stats['Team Stats'] != 'Penalties')]

    if side == 'offense':
        stats_name[team_prefix] = stats_name[team_prefix].astype(float)
        pivot = stats_name.pivot_table(columns = 'Team Stats', values = team_prefix, aggfunc=stat_type)
    elif side == 'defense':
        stats_name[team_prefix + '_' + "Opponent"] = stats_name[team_prefix + '_' + "Opponent"].astype(float)
        pivot = stats_name.pivot_table(columns = 'Team Stats', values = team_prefix + '_' + "Opponent", aggfunc=stat_type)
    
    if project_name != None:
        pivot.to_csv(save_folder + '/' + project_name + '_' + side +'.csv')
    return pivot
  
 ### Example

'''
ravens_o = get_statistics('Ravens', 'BAL','offense', 'mean')
bengals_o = get_statistics('Bengals', 'CIN', 'offense', 'mean')
ravens_d = get_statistics('Ravens','BAL', 'defense', 'mean')
bengals_d = get_statistics('2Bengals', 'CIN', 'defense', 'mean')

matchup  = pd.concat([ravens_o, bengals_o, ravens_d, bengals_d])

matchup
'''
