
class Calendario:
    def __init__(self, giornate):
        '''
        giornate: lista di oggetti Giornata
        '''
        self.giornate = giornate
    
    def get_teams(self):
        '''
        restituisce lista con nomi delle squadre
        '''
        giornata = self.giornate[0]
        teams = []
        for m in giornata.get_matches():
            teams.append(m[0])
            teams.append(m[1])
        
        return teams
    

    def get_team_points_map(self):
        '''
        restituisce un dizionario con
        key: nome squadra
        value: lista di punti in classifica ad ogni giornata
        '''

        giornate = self.giornate
        teams = self.get_teams()

        tps_map = {t: [0] for t in teams}
        for g in giornate:
            for t, p in g.get_team_point_map().items():
                tps_map[t].append(tps_map[t][-1] + p)
        
        return tps_map
    
    def get_team_f1points_map(self):
        '''
        restituisce un dizionario con
        key: nome squadra
        value: lista di punti in classifica ad ogni giornata
        '''

        giornate = self.giornate
        teams = self.get_teams()

        tf1ps_map = {t: [0] for t in teams}
        for g in giornate:
            for t, p in g.get_team_f1point_map().items():
                tf1ps_map[t].append(tf1ps_map[t][-1] + p)
        
        return tf1ps_map
