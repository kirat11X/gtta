import math
import random
import itertools

def main():
    print("=" * 50)
    print("TABLE TENNIS FIXTURE GENERATOR")
    print("=" * 50)
    
    # Step 1: Tournament format selection
    print("\n🟠 Step 1: Select Tournament Format")
    print("1. Knockout")
    print("2. League")
    print("3. League-cum-Knockout")
    print("4. Knockout-cum-League")
    
    format_choice = int(input("Enter format number (1-4): "))
    formats = {
        1: "Knockout",
        2: "League",
        3: "League-cum-Knockout",
        4: "Knockout-cum-League"
    }
    selected_format = formats.get(format_choice, "Knockout")
    print(f"Selected format: {selected_format}")
    
    # Step 2: Basic inputs based on format
    if selected_format in ["Knockout", "Knockout-cum-League"]:
        num_players = int(input("\n🟠 Step 2: Enter total number of players: "))
        num_groups = 0
    else:
        num_players = int(input("\n🟠 Step 2: Enter total number of players: "))
        num_groups = int(input("Enter number of groups: "))
    
    # Step 3: Player details
    print("\n🟠 Step 3: Enter Player Names")
    players = []
    for i in range(num_players):
        player_name = input(f"Player {i+1} name: ")
        players.append(player_name)
    
    # Step 4: Seeding inputs
    print("\n🟠 Step 4: Seeding Information")
    seed_options = [2, 4, 8,0]
    num_seeds = 0
    seeded_players = {}
    
    while num_seeds not in seed_options:
        num_seeds = int(input("Enter number of seeded players (0,2, 4, or 8): "))
        if num_seeds not in seed_options:
            print("Invalid number. Please enter 0, 2, 4, or 8.")
    
    print("\nSelect players and assign seed ranks:")
    for rank in range(1, num_seeds + 1):
        print(f"\nAvailable players: {', '.join(players)}")
        seed_name = input(f"Enter name for seed #{rank}: ")
        while seed_name not in players:
            print("Invalid player name. Please choose from the list.")
            seed_name = input(f"Enter name for seed #{rank}: ")
        seeded_players[rank] = seed_name
        players.remove(seed_name)
    
    # Add unseeded players back to the player pool
    players = list(seeded_players.values()) + players
    
    # Step 5: Generate fixtures based on format
    print("\n" + "=" * 50)
    print("GENERATED FIXTURES")
    print("=" * 50)
    
    if selected_format == "Knockout":
        knockout_fixtures(players, seeded_players)
    elif selected_format == "League":
        league_fixtures(players, seeded_players, num_groups)
    elif selected_format == "League-cum-Knockout":
        league_cum_knockout(players, seeded_players, num_groups)
    else:
        knockout_cum_league(players, seeded_players, num_groups)

def knockout_fixtures(players, seeded_players):
    num_players = len(players)
    n = math.ceil(math.log2(num_players))
    total_slots = 2 ** n
    byes = total_slots - num_players
    
    print(f"\nKnockout Tournament with {num_players} players")
    print(f"Total slots: {total_slots}, Byes: {byes}")
    
    # Create bracket slots
    bracket = [None] * total_slots
    
    # Predefined bye positions
    bye_positions = [
        2,                  # 1st bye position
        total_slots - 1,     # 2nd bye position
        (2 ** (n-1)) + 2,   # 3rd bye position
        (2 ** (n-1)) - 1,   # 4th bye position
        (2 ** (n-2)) + 2,   # 5th bye position
        (3 * 2 ** (n-2)) - 1,  # 6th bye position
        (3 * 2 ** (n-2)) + 2,  # 7th bye position
        (2 ** (n-2)) - 1    # 8th bye position
    ]
    
    # Assign byes
    for i in range(min(byes, 8)):
        bracket[bye_positions[i] - 1] = "BYE"
    
    # Assign remaining byes randomly
    available_slots = [i for i in range(total_slots) if bracket[i] is None]
    for _ in range(byes - 8):
        if available_slots:
            pos = random.choice(available_slots)
            bracket[pos] = "BYE"
            available_slots.remove(pos)
    
    # Place seeded players
    seed_positions = {
        1: 0,                           # Top of bracket
        2: total_slots - 1,              # Bottom of bracket
        3: total_slots // 4 - 1,         # Quarter 1
        4: 3 * total_slots // 4,         # Quarter 4
        5: total_slots // 8,             # Eighth 1
        6: 3 * total_slots // 8,         # Eighth 3
        7: 5 * total_slots // 8,         # Eighth 5
        8: 7 * total_slots // 8          # Eighth 7
    }
    
    for rank, player in seeded_players.items():
        if rank in seed_positions:
            pos = seed_positions[rank]
            if bracket[pos] is None or bracket[pos] == "BYE":
                bracket[pos] = player
    
    # Place remaining players randomly
    unseeded = [p for p in players if p not in seeded_players.values()]
    random.shuffle(unseeded)
    
    for i in range(total_slots):
        if bracket[i] is None:
            if unseeded:
                bracket[i] = unseeded.pop()
            else:
                bracket[i] = "BYE"
    
    # Display bracket
    print("\nKnockout Bracket:")
    round_slots = total_slots
    round_num = 1
    current_bracket = bracket.copy()
    
    while round_slots >= 1:
        print(f"\n--- Round {round_num} ---")
        for i in range(0, round_slots, 2):
            player1 = current_bracket[i]
            player2 = current_bracket[i+1] if i+1 < len(current_bracket) else "BYE"
            print(f"Match {i//2 + 1}: {player1} vs {player2}")
        
        # Prepare next round
        next_round = []
        for i in range(0, round_slots, 2):
            winner = f"Winner {i//2 + 1}"
            next_round.append(winner)
        
        current_bracket = next_round
        round_slots //= 2
        round_num += 1

def league_fixtures(players, seeded_players, num_groups):
    print(f"\nLeague Tournament with {len(players)} players in {num_groups} groups")
    
    # Distribute seeded players
    groups = [[] for _ in range(num_groups)]
    seed_ranks = sorted(seeded_players.keys())
    
    for rank in seed_ranks:
        group_idx = (rank - 1) % num_groups
        groups[group_idx].append(seeded_players[rank])
    
    # Distribute remaining players
    unseeded = [p for p in players if p not in seeded_players.values()]
    random.shuffle(unseeded)
    
    group_idx = 0
    while unseeded:
        groups[group_idx].append(unseeded.pop())
        group_idx = (group_idx + 1) % num_groups
    
    # Generate fixtures for each group
    for group_num, group_players in enumerate(groups, 1):
        print(f"\nGroup {group_num}: {', '.join(group_players)}")
        print("Fixtures:")
        
        fixtures = list(itertools.combinations(group_players, 2))
        random.shuffle(fixtures)
        
        for i, (player1, player2) in enumerate(fixtures, 1):
            print(f"Match {i}: {player1} vs {player2}")

def league_cum_knockout(players, seeded_players, num_groups):
    print("\nLEAGUE-CUM-KNOCKOUT TOURNAMENT")
    print("Phase 1: League Stage")
    league_fixtures(players, seeded_players, num_groups)
    
    print("\nPhase 2: Knockout Stage")
    # Top 2 from each group advance
    knockout_players = []
    for group_num in range(num_groups):
        knockout_players.append(f"Group {group_num+1} Winner")
        knockout_players.append(f"Group {group_num+1} Runner-up")
    
    # Create a temporary seeding for knockout
    temp_seeds = {1: knockout_players[0], 2: knockout_players[1]}
    if len(knockout_players) > 2:
        temp_seeds[3] = knockout_players[2]
    if len(knockout_players) > 3:
        temp_seeds[4] = knockout_players[3]
    
    knockout_fixtures(knockout_players, temp_seeds)

def knockout_cum_league(players, seeded_players, num_groups):
    print("\nKNOCKOUT-CUM-LEAGUE TOURNAMENT")
    print("Phase 1: Knockout Stage")
    # First round knockout
    num_players = len(players)
    n = math.ceil(math.log2(num_players))
    total_slots = 2 ** n
    winners = [f"Match {i+1} Winner" for i in range(total_slots // 2)]
    
    print("\nPhase 2: League Stage")
    league_fixtures(winners, {}, num_groups)

if __name__ == "__main__":
    main()