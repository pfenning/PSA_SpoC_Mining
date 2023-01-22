elif method == 'test':
        import pykep as pk
        data = np.loadtxt("SpoC_Datensatz.txt")

        T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs
        T_END = pk.epoch_from_iso_string("30240302T000000")
        T_DAUER = 1827
        G = 6.67430e-11  # Cavendish constant (m^3/s^2/kg)
        SM = 1.989e30  # Sun_mass (kg)
        MS = 8.98266512e-2 * SM  # Mass of the Trappist-1 star
        MU_TRAPPIST = G * MS  # Mu of the Trappist-1 star
        DV_per_propellant = 10000  # DV per propellant [m/s]
        TIME_TO_MINE_FULLY = 30  # Maximum time to fully mine an asteroid
        t_opt = 0.0

        asteroids_kp = []
        for line in data:
            p = pk.planet.keplerian(
                T_START,
                (
                    line[1],
                    line[2],
                    line[3],
                    line[4],
                    line[5],
                    line[6],
                ),
                MU_TRAPPIST,
                G * line[7],  # mass in planet is not used in UDP, instead separate array below
                1,  # these variable are not relevant for this problem
                1.1,  # these variable are not relevant for this problem
                "Asteroid " + str(int(line[0])),
            )
            asteroids_kp.append(p)

        # entire_ids = asteroids_kp[:,0]

        '''
        Vorgabe des ersten und zweiten Asteroiden!!
        Insbesondere der zweite Asteroid ist von Bedeutung
        ==> Rückwirkenden Branch erstellen!! 
        '''

        # 1) den ZWEITEN Asteroiden finden, aus minimaler Verfügbarkeit und maximaler Masse
        ast_2_idx_v = []
        min_mat_mass = []
        min_mat = find_min_material(data)
        for i in range(0, len(data)):
            if data[i, -1] == min_mat:
                min_mat_mass.append(data[i, -2])
                ast_2_idx_v.append(data[i, 0])
        second_asteroid = np.argpartition(min_mat_mass, -1)[-1:]  # Vektor mit Index
        asteroid_2_idx = int(ast_2_idx_v[second_asteroid[0]])
        asteroid_2_masse = min_mat_mass[second_asteroid[0]]
        print(asteroid_2_idx, asteroid_2_masse)
        # entire_ids.pop(asteroid_2_idx)

        # 2) Cluster um zweiten Asteroiden bilden, ERSTEN Asteroiden auswählen mit minimalem Abstand!!
        knn = phasing.knn(asteroids_kp, t_opt, 'orbital',
                          T=15)  # wie wähle ich t_arr und t_opt?  # visited[-1]['t_arr'] + t_opt
        neighb_ind = SpoC.clustering(knn, asteroids_kp, asteroid_2_idx)
        # Den zweiten Ast.-Idx rausschmeißen
        if asteroid_2_idx in neighb_ind: neighb_ind.pop(neighb_ind.index(asteroid_2_idx))

        # print(neighb_ind) # die neighb_dis ist immer "None" !!!!! DAS KÖNNTE AUSWAHL VERBESSERN

        possible_steps = []
        for mat in neighb_ind:
            # print(mat)
            # print(data[mat,-1])
            if data[mat, -1] == 3: possible_steps.append(mat)

        # print(possible_steps)

        # 3) FALSCH HERUM BRANCH LAUFEN LASSEN
        infos_poss_steps = []
        DVs = []
        for ast_1 in possible_steps:
            asteroid_1_kp = asteroids_kp[ast_1]
            asteroid_1_mas = data[ast_1, -2]
            asteroid_1_mat = data[ast_1, -1]
            asteroid_2_kp = asteroids_kp[asteroid_2_idx]
            t_m_opt_, t_flug_min_dv_, dv_min_ = SpoC.time_optimize(asteroid_1_kp,
                                                                  asteroid_1_mas,
                                                                  asteroid_1_mat,
                                                                  asteroid_2_kp,
                                                                  t_arr=0.0,
                                                                  t_opt=t_opt,
                                                                  limit=1.0)
            infos_poss_steps.append([t_m_opt_, t_flug_min_dv_, dv_min_])
            DVs.append(dv_min_)

        idx_min_dv = DVs.index(min(DVs))
        asteroid_1_idx = possible_steps[idx_min_dv]

        t_m_opt_, t_flug_min_dv_, dv_min_ = infos_poss_steps[idx_min_dv][0], infos_poss_steps[idx_min_dv][1], \
        infos_poss_steps[idx_min_dv][2]

        t_m = t_m_opt_
        step = {'id': asteroid_2_idx,
                't_m': 0.0,
                't_arr': t_m_opt_ + t_flug_min_dv_,
                'score last step': 0.0,  # score??
                'branch score yet': 0.0}
        dv = dv_min_

        # 4) Branch erstellen
        asteroid1 = Seed(asteroid_1_idx,fuzzy=fuzzy)
        start_branches.append(
            ExpandBranch(asteroid1,
                         asteroid_id=asteroid_2_idx,
                         last_t_m=0.0, dv=dv_min_,
                         t_arr=t_m_opt_ + t_flug_min_dv_,
                         step_score=0.0,fuzzy=fuzzy))
        print(start_branches[0])
