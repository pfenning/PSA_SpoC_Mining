from branch_class import Branch
class ExpandBranch:
    def __init__(self, origin_branch, new_step):
        """
        Objekt, zum Speichern des Expand-Schrittes in Beam-Search-Algorithmus.
        Speicher nur eine Referenz des zu erweiternden Branches, sowie den möglichen Expand-Schritt.
        :type origin_branch:    Branch
        :type new_step:         dict
        :param origin_branch:   Pfad, der Erweitert werden soll
        :param new_step:        Expand-Schritt
        """
        self.origin_branch = origin_branch
        if False in [key in new_step for key in ['id', 't_m', 't_arr', 'score last step', 'branch score yet']]:
            raise ValueError("step has not all keys needed")
        else:
            self.new_step = new_step

    def get_score(self):
        """
        Gibt den Score des Expand-Schritts zurück
        :return: Score des Expand-Schritts
        """
        return self.new_step['score last step']

    def get_branch_score(self):
        """
        Gibt den Branch-Score, also den Mittelwert der Step-Scores, für den erweiterten Branch zurück
        :return: Branch-Score des erweiterten Branches
        """
        return (len(self.origin_branch.visited)*self.origin_branch.get_branch_score()+self.get_score())/\
            (len(self.origin_branch.visited)+1)

    def get_expanded_branch(self):
        """
        Gibt Branch-Objekt zurück, dass Expand-Schritt enthält
        :return: Branch-Objekt zurück, dass Expand-Schritt enthält
        """
        pass