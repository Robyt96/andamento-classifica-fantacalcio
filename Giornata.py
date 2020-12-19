
class Giornata:
    def __init__(self, df):
        '''
        df: dataframe
        '''
        self.df = df
        self.f1_rank_points = [15,12,10,8,6,4,2,1]
    

    def get_team_gols_map(self):
        '''
        restituisce dizionario con
        key: nome squadra
        value: gol segnati
        '''

        df = self.df

        team_gol_map = {}
        for row in range(df.shape[0]):
            gol = [int(g) for g in df.iloc[row, 4].split('-')]
            team_gol_map[df.iloc[row, 0]], team_gol_map[df.iloc[row, 3]] = gol
        
        return team_gol_map
    

    def get_matches(self):
        '''
        restituisce lista di tuple. ogni tupla contiene i nomi di due squadre
        che si sono affrontate nella giornata
        '''

        df = self.df
        matches = [(df.iloc[row, 0], df.iloc[row, 3]) for row in range(df.shape[0])]
        return matches
    

    def get_team_point_map(self):
        '''
        restituisce dizionario con
        key: nome squadra
        value: punti fatti (3, 1 o 0)
        '''

        tg_map = self.get_team_gols_map()
        matches = self.get_matches()

        tp_map = {}
        for m in matches:
            t1, t2 = m
            if (tg_map[t1] > tg_map[t2]):
                tp_map[t1] = 3
                tp_map[t2] = 0
            elif (tg_map[t1] < tg_map[t2]):
                tp_map[t1] = 0
                tp_map[t2] = 3
            else:
                tp_map[t1] = 1
                tp_map[t2] = 1
        
        return tp_map
    

    def get_team_fantapoints_map(self):
        '''
        restituisce dizionario con
        key: nome della squadra
        value: fantapunteggio realizzato
        '''

        df = self.df

        tf_map = {}
        for row in range(df.shape[0]):
            tf_map[df.iloc[row, 0]] = df.iloc[row, 1]
            tf_map[df.iloc[row, 3]] = df.iloc[row, 2]
        
        return tf_map
    

    def get_team_f1point_map(self):
        '''
        restituisce dizionario con
        key: nome della squadra
        value: punteggio realizzato con il meccanismo Formula 1
        '''
        
        f1_rank_points = self.f1_rank_points
        tfp = self.get_team_fantapoints_map()
        # creo lista di tuple (squadra, fantapunti)
        teams_fp_list = [(key, value) for key, value in tfp.items()]
        ordered_teams_fp_list = sorted(teams_fp_list, key=lambda tup: tup[1], reverse=True)

        team_f1points = {}
        team_f1points[ordered_teams_fp_list[0][0]] = f1_rank_points[0]
        for tup in range(1, len(ordered_teams_fp_list)):
            # se a parimerito nell'ordinamento
            if (ordered_teams_fp_list[tup][1] == ordered_teams_fp_list[tup-1][1]):
                team_f1points[ordered_teams_fp_list[tup][0]] = f1_rank_points[tup-1]
            # altrimenti
            else:
                team_f1points[ordered_teams_fp_list[tup][0]] = f1_rank_points[tup]
        
        return team_f1points
