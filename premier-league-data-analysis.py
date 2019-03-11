# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 10:56:23 2019

@author: sambu
"""

import pandas as pd

def get_user_input():
    
    print('Hello! Let\'s explore some English Premier League data from the 1993-94 to the 2017-18 season!')
    print('Would you like to see data for 1) Any particular Club, 2) Any particular Season, 3) All Clubs, 4) All Seasons - Please enter 1, 2, 3 or 4 as choice')
    
    invalidinput = False
    choice = ''
    club = ''
    season = ''
    
    while choice == '' or invalidinput:
        choice = input()
        if choice != '1' and choice != '2' and choice != '3' and choice != '4':
            invalidinput = True
            print ('Invalid Input! Please enter correct input...')
        else:
            invalidinput = False
    
    df_eplscore = pd.read_csv('EPL_Set.csv')
            
    if choice == '1':
        print ('Please enter the club name')
        invalidinput = False

        
        while club == '' or invalidinput:
            club = input()
            
            club_names = get_unique_clubnames(df_eplscore)
            season = 'ALL'
            
            if club not in club_names:
                invalidinput = True
                print ('Invalid Input! Please enter correct input...')
            else:
                invalidinput = False
                
    elif choice == '2':
        print ('Please enter the season name in the format XXXX-XX i.e. 2002-03')
        invalidinput = False        
        
        while season == '' or invalidinput:
            season = input()
            
            season_names = get_unique_seasonnames(df_eplscore)
            
            if season not in season_names:
                invalidinput = True
                print ('Invalid Input! Please enter correct input...')
            else:
                invalidinput = False
                
    return df_eplscore, choice, club, season
            


def get_unique_clubnames(df_eplscore):
    
    club_names = df_eplscore['HomeTeam'].unique()
    
    return club_names

def get_unique_seasonnames(df_eplscore):
    
    season_names = df_eplscore['Season'].unique()
    
    return season_names

def count_total_team_result (df_eplscore, club, season):
    i = 0
    homeWinCount = 0
    awayWinCount = 0
    homeDefeatCount = 0
    awayDefeatCount = 0
    homeDrawCount = 0
    awayDrawCount = 0
    goalsscored = 0
    goalsconceded = 0
    while i < len(df_eplscore):
        if df_eplscore['HomeTeam'][i] == club and (season.upper() == 'ALL' or str(df_eplscore['Season'][i]) == season):
            goalsscored += df_eplscore['FTHG'][i]
            goalsconceded += df_eplscore['FTAG'][i]
            if df_eplscore['FTR'][i] == 'H':
                homeWinCount += 1
            elif df_eplscore['FTR'][i] == 'A':
                homeDefeatCount += 1
            else:
                homeDrawCount += 1
        elif df_eplscore['AwayTeam'][i] == club and (season.upper() == 'ALL' or str(df_eplscore['Season'][i]) == season):
            goalsscored += df_eplscore['FTAG'][i]
            goalsconceded += df_eplscore['FTHG'][i]            
            if df_eplscore['FTR'][i] == 'A':
                awayWinCount += 1
            elif df_eplscore['FTR'][i] == 'H':
                awayDefeatCount += 1
            else:
                awayDrawCount += 1
        i += 1
        
    return homeWinCount, homeDefeatCount, homeDrawCount, awayWinCount, awayDefeatCount, awayDrawCount, goalsscored, goalsconceded
            

def get_team_points_for_season (df_eplscore, club, season):
    
    pointsTotal = 0
    homeWinCount, homeDefeatCount, homeDrawCount, awayWinCount, awayDefeatCount, awayDrawCount, goalsscored, goalsconceded = count_total_team_result (df_eplscore, club, season)
    pointsTotal += homeWinCount*3 + homeDrawCount + awayWinCount*3 + awayDrawCount
    return pointsTotal

def final_league_table_for_season (df_eplscore, season):
    
    list_of_clubs = df_eplscore['HomeTeam'].unique()
    
    totalPlayedList = []
    totalWinList = []
    totalDefeatList = []
    totalDrawList = []
    totalPointsList = []
    participatingClubList = []
    goalscoredList = []
    goalconcededList = []
    goaldifferenceList = []
    
    for i in range(len(list_of_clubs)):
        homeWinCount, homeDefeatCount, homeDrawCount, awayWinCount, awayDefeatCount, awayDrawCount, goalsscored, goalsconceded = count_total_team_result(df_eplscore, list_of_clubs[i], season)
        
        totalPlayed = homeWinCount + homeDefeatCount + homeDrawCount + awayWinCount + awayDefeatCount + awayDrawCount
        if totalPlayed == 0:
            continue
        
        pointsTotal = homeWinCount*3 + homeDrawCount + awayWinCount*3 + awayDrawCount
        totalWin = homeWinCount + awayWinCount
        totalDefeat = homeDefeatCount + awayDefeatCount
        totalDraw = homeDrawCount + awayDrawCount
        goaldifference = goalsscored - goalsconceded        
        
        totalPlayedList.append(totalPlayed)
        totalWinList.append(totalWin)
        totalDefeatList.append(totalDefeat)
        totalDrawList.append(totalDraw)
        totalPointsList.append(pointsTotal)
        participatingClubList.append(list_of_clubs[i])
        goalscoredList.append(goalsscored)
        goalconcededList.append(goalsconceded)
        goaldifferenceList.append(goaldifference)
        
        i += 1
        

    df_final_league_table = pd.DataFrame({'Played' : pd.Series(data = totalPlayedList, index = participatingClubList),
                                    'Won' : pd.Series(data = totalWinList, index = participatingClubList),
                                    'Drawn' : pd.Series(data = totalDrawList, index = participatingClubList),
                                    'Lost' : pd.Series(data = totalDefeatList, index = participatingClubList),
                                    'GF' : pd.Series(data = goalscoredList, index = participatingClubList),
                                    'GA' : pd.Series(data = goalconcededList, index = participatingClubList),
                                    'GD' : pd.Series(data = goaldifferenceList, index = participatingClubList),
                                    'Points' : pd.Series(data = totalPointsList, index = participatingClubList)})
    
    df_final_league_table.sort_values(by = ['Points', 'GD', 'GF'], inplace=True, ascending=False)
    
    return df_final_league_table

def get_team_standing_season_by_season (df_eplscore, club):
    
    list_of_seasons = df_eplscore['Season'].unique()
    
    totalPlayedList = []
    totalWinList = []
    totalDefeatList = []
    totalDrawList = []
    totalPointsList = []
    clubSeasonList = []
    goalscoredList = []
    goalconcededList = []
    goaldifferenceList = []
    
    for i in range(len(list_of_seasons)):
        homeWinCount, homeDefeatCount, homeDrawCount, awayWinCount, awayDefeatCount, awayDrawCount, goalsscored, goalsconceded = count_total_team_result (df_eplscore, club, list_of_seasons[i])
        
        totalPlayed = homeWinCount + homeDefeatCount + homeDrawCount + awayWinCount + awayDefeatCount + awayDrawCount
        
        if totalPlayed == 0:
            continue
        
        pointsTotal = homeWinCount*3 + homeDrawCount + awayWinCount*3 + awayDrawCount
        totalWin = homeWinCount + awayWinCount
        totalDefeat = homeDefeatCount + awayDefeatCount
        totalDraw = homeDrawCount + awayDrawCount
        goaldifference = goalsscored - goalsconceded        
        
        totalPlayedList.append(totalPlayed)
        totalWinList.append(totalWin)
        totalDefeatList.append(totalDefeat)
        totalDrawList.append(totalDraw)
        totalPointsList.append(pointsTotal)
        clubSeasonList.append(list_of_seasons[i])
        goalscoredList.append(goalsscored)
        goalconcededList.append(goalsconceded)
        goaldifferenceList.append(goaldifference)
        
        i += 1
        
    print ('Premier League Season by Season Standing for ', club)
    df_season_by_season_table = pd.DataFrame({'Played' : pd.Series(data = totalPlayedList, index = clubSeasonList),
                                    'Won' : pd.Series(data = totalWinList, index = clubSeasonList),
                                    'Drawn' : pd.Series(data = totalDrawList, index = clubSeasonList),
                                    'Lost' : pd.Series(data = totalDefeatList, index = clubSeasonList),
                                    'GF' : pd.Series(data = goalscoredList, index = clubSeasonList),
                                    'GA' : pd.Series(data = goalconcededList, index = clubSeasonList),
                                    'GD' : pd.Series(data = goaldifferenceList, index = clubSeasonList),
                                    'Points' : pd.Series(data = totalPointsList, index = clubSeasonList)})
        
    return df_season_by_season_table


def main():

    while True:
        df_eplscore, choice, club, season = get_user_input()       
        
        club_names = get_unique_clubnames(df_eplscore)
        season_names = get_unique_clubnames(df_eplscore)
        
        if choice == '1':
            df_season_by_season_table = get_team_standing_season_by_season (df_eplscore, club)
            print(df_season_by_season_table)
            
            homeWinCount, homeDefeatCount, homeDrawCount, awayWinCount, awayDefeatCount, awayDrawCount, goalsscored, goalsconceded = count_total_team_result (df_eplscore, club, 'ALL')
            print ('All time stats for club ' , club)
            print ('Home Wins: ', homeWinCount, 'Home Defeats: ', homeDefeatCount, 'Home Draws: ', homeDrawCount, 'Away Wins: ', awayWinCount, 'Away Defeats: ', awayDefeatCount, 'Away Draws: ', awayDrawCount, 'Goals Scored: ', goalsscored, 'Goals Scored: ', goalsconceded)
        
        elif choice == '2':
            df_final_league_table = final_league_table_for_season(df_eplscore, season)
            print(df_final_league_table)
            
        elif choice == '3':
            print ('All clubs who participated so far in Premier League: ', club_names)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thats all for now - have a great day!')
            break
            

if __name__ == "__main__":
	main()