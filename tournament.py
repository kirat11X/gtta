import math
import random
import itertools

def main():
    print("=" * 50)
    print("TABLE TENNIS FIXTURE GENERATOR")
    print("=" * 50)
    
    # Step 1: Tournament format selection (removed hybrid formats)
    print("\n🟠 Step 1: Select Tournament Format")
    print("1. Knockout")
    print("2. League")
    
    format_choice = int(input("Enter format number (1-2): "))
    formats = {
        1: "Knockout",
        2: "League"
    }
    selected_format = formats.get(format_choice, "Knockout")
    print(f"Selected format: {selected_format}")
    
    # Step 2: Basic inputs based on format
    if selected_format == "Knockout":
        num_players = int(input("\n🟠 Step 2: Enter total number of players: "))
        num_groups = 0
    else:  # League format
        num_players = int(input("\n🟠 Step 2: Enter total number of players: "))
        num_groups = int(input("Enter number of groups: "))
    
    # Step 3: Player details
    print("\n🟠 Step 3: Enter Player Names")
    players = []
    for i in range(num_players):
        player_name = input(f"Player {i+1} name: ")
        players.append(player_name)
    
    # Step 4: Seeding inputs with option for 0 seeds
    print("\n🟠 Step 4: Seeding Information")
    seeded_players = {}
    
    num_seeds = -1
    while num_seeds < 0 or num_seeds > 8:
        num_seeds = int(input("Enter number of seeded players (0, 2, 4, or 8): "))
        if num_seeds not in [0, 2, 4, 8]:
            print("Invalid number. Please enter 0, 2, 4, or 8.")
    
    if num_seeds > 0:
        print("\nSelect players and assign seed ranks:")
        for rank in range(1, num_seeds + 1):
            print(f"\nAvailable players: {', '.join(players)}")
            seed_name = input(f"Enter name for seed #{rank}: ")
            while seed_name not in players:
                print("Invalid player name. Please choose from the list.")
                seed_name = input(f"Enter name for seed #{rank}: ")
            seeded_players[rank] = seed_name
            players.remove(seed_name)
    
    # Add seeded players back to the player pool
    players = list(seeded_players.values()) + players
    
    # Step 5: Generate fixtures based on format
    print("\n" + "=" * 50)
    print("GENERATED FIXTURES")
    print("=" * 50)
    
    if selected_format == "Knockout":
        knockout_fixtures(players, seeded_players)
    else:  # League format
        league_fixtures(players, seeded_players, num_groups)

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
    bye_positions = []
    if n >= 1:
        bye_positions.append(2)  # 1st bye position
    if n >= 2:
        bye_positions.append(total_slots - 1)  # 2nd bye position
    if n >= 3:
        bye_positions.append((2 ** (n-1)) + 2)  # 3rd bye position
        bye_positions.append((2 ** (n-1)) - 1)  # 4th bye position
    if n >= 4:
        bye_positions.append((2 ** (n-2)) + 2)  # 5th bye position
        bye_positions.append((3 * 2 ** (n-2)) - 1)  # 6th bye position
        bye_positions.append((3 * 2 ** (n-2)) + 2)  # 7th bye position
        bye_positions.append((2 ** (n-2)) - 1)  # 8th bye position
    
    # Assign byes using predefined positions first
    for i in range(min(byes, len(bye_positions))):
        pos_index = bye_positions[i] - 1
        if pos_index < len(bracket):
            bracket[pos_index] = "BYE"
    
    # Assign remaining byes randomly if needed
    available_slots = [i for i in range(total_slots) if bracket[i] is None]
    random.shuffle(available_slots)
    for _ in range(max(0, byes - len(bye_positions))):
        if available_slots:
            pos = available_slots.pop()
            bracket[pos] = "BYE"
    
    # Place seeded players if any
    seed_positions = {}
    if seeded_players:
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
            if pos < len(bracket) and (bracket[pos] is None or bracket[pos] == "BYE"):
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
    
    while round_slots >= 2:
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
    
    # Place seeds in different groups
    for rank in seed_ranks:
        group_idx = (rank - 1) % num_groups
        groups[group_idx].append(seeded_players[rank])
    
    # Distribute remaining players
    unseeded = [p for p in players if p not in seeded_players.values()]
    random.shuffle(unseeded)
    
    # Fill groups with remaining players
    while unseeded:
        # Find group with fewest players
        min_size = min(len(group) for group in groups)
        for group in groups:
            if len(group) == min_size:
                group.append(unseeded.pop())
                break
    
    # Generate fixtures for each group
    for group_num, group_players in enumerate(groups, 1):
        group_size = len(group_players)
        print(f"\nGroup {group_num} ({group_size} players): {', '.join(group_players)}")
        
        # Generate all possible matches
        fixtures = list(itertools.combinations(group_players, 2))
        random.shuffle(fixtures)
        
        print("\nFixture Schedule:")
        for match_num, (player1, player2) in enumerate(fixtures, 1):
            print(f"Match {match_num}: {player1} vs {player2}")
        
        # # Calculate total matches per player
        # matches_per_player = {player: 0 for player in group_players}
        # for p1, p2 in fixtures:
        #     matches_per_player[p1] += 1
        #     matches_per_player[p2] += 1
        
        # print("\nMatches per player:")
        # for player, count in matches_per_player.items():
        #     print(f"{player}: {count} matches")

if __name__ == "__main__":
    main()