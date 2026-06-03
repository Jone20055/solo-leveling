import time
import random

class SoloLevelingArcade:
    def __init__(self):
        # Core Player Stats & Multipliers
        self.level, self.xp, self.max_xp, self.stat_points, self.floor = 1, 0, 100, 0, 0
        self.stats = {"power": 0, "defence": 0, "speed": 0, "mana": 0}
        self.mana, self.gold, self.weapon, self.weapon_bonus = 10, 0, "Bare Fists", 0
        self.shadow_ranks = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Chroma"]
        self.shadow_prices = {"Common": 10, "Uncommon": 50, "Rare": 250, "Epic": 1000, "Legendary": 5000, "Chroma": 50000}
        self.shadows = {r: 0 for r in self.shadow_ranks}
        self.log = "System Core Online. Welcome, Shadow Monarch."
        self.start_time = time.time()

    def sync_passive_xp(self):
        """Calculates 1 second = 1 XP using the browser's live internal clock"""
        elapsed = int(time.time() - self.start_time)
        if elapsed > 0:
            self.xp += elapsed
            self.start_time = time.time()
            while self.xp >= self.max_xp:
                self.xp -= self.max_xp
                self.level += 1
                self.stat_points += 30
                self.max_xp = int(self.max_xp * 1.4)
                self.log = f"✨ LEVEL UP! You reached Level {self.level}! +30 Stat Points."
                # Auto unlock weapons matching level tiers
                w_tiers = {5: ("Steel Dagger", 15), 15: ("Knight Killer", 50), 30: ("Baran's Shortsword", 150), 60: ("Kamish's Wrath", 800)}
                for lvl, (name, bonus) in w_tiers.items():
                    if self.level >= lvl and name not in self.weapon:
                        self.weapon, self.weapon_bonus = name, bonus

    # Player Multiplier Logic Rules
    def get_max_hp(self): return int(100 * (2 ** (self.stats["defence"] / 10)))
    def get_total_atk(self): return int((15 + self.weapon_bonus) * (2 ** (self.stats["power"] / 10)))
    def get_dodge(self): return min(90, int((self.stats["speed"] / 10) * 10))

    def show_dashboard(self):
        self.sync_passive_xp()
        print("\n" + "⚡" * 32)
        print(f"👑 MONARCH LVL: {self.level} [{self.xp}/{self.max_xp} XP] | 🏰 CURRENT FLOOR: {self.floor}")
        print(f"❤️ MAX HEALTH: {self.get_max_hp()} HP | ⚔️ STRIKE DAMAGE: {self.get_total_atk()} ATK")
        print(f"👟 AUTO-DODGE: {self.get_dodge()}% | 💰 GOLD WALLET: {self.gold}G | 💧 MANA: {self.mana} MP")
        print(f"📊 UNASSIGNED STAT POINTS: {self.stat_points}")
        print("─" * 64)
        active_army = [f"{k}: {v}" for k, v in self.shadows.items() if v > 0]
        print(f"🔮 ACTIVE ARMY: " + (", ".join(active_army) if active_army else "No shadows summoned yet."))
        print(f"⚔️ WEAPON EQUIPPED: {self.weapon} (+{self.weapon_bonus} ATK)")
        print("─" * 64)
        print(f"📢 SYSTEM NOTICE: {self.log}")
        print("⚡" * 32)

    def allocate_stats(self):
        if self.stat_points <= 0: self.log = "❌ You have no stat points to spend right now."; return
        print("\n[📊 SELECT DIRECTION TO INJECT POINTS]")
        print(f"1. Power (+2x Damage) | 2. Defence (+2x HP) | 3. Speed (+10% Dodge) | 4. Mana")
        choice = input("Enter Stat Number (1-4): ").strip()
        amt = input(f"How many points? (Max {self.stat_points}): ").strip()
        if amt.isdigit() and 0 < int(amt) <= self.stat_points:
            mapping = {"1": "power", "2": "defence", "3": "speed", "4": "mana"}
            if choice in mapping:
                self.stats[mapping[choice]] += int(amt)
                self.stat_points -= int(amt)
                self.log = f"✅ Successfully added {amt} points to {mapping[choice].upper()}!"

    def shadow_shop(self):
        print("\n[🛒 SHADOW EXTRACTOR SHOP]")
        for i, rank in enumerate(self.shadow_ranks):
            print(f" {i+1}. Extract {rank} Soldier ➔ Cost: {self.shadow_prices[rank]} MP")
        choice = input("Enter Item Number to Buy (0 to Cancel): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(self.shadow_ranks):
            rank = self.shadow_ranks[int(choice)-1]
            if self.mana >= self.shadow_prices[rank]:
                self.mana -= self.shadow_prices[rank]
                self.shadows[rank] += 1
                self.log = f"🔮 ARISE! A new [{rank}] shadow soldier has been extracted!"
            else: self.log = "❌ Insufficient Mana points to execute extraction."

    def merge_engine(self):
        print("\n[🧬 ARMY EVOLUTION FUSION ENGINE]")
        merges = {"Common": (5, "Uncommon"), "Uncommon": (5, "Rare"), "Rare": (4, "Epic"), "Epic": (5, "Legendary"), "Legendary": (4, "Chroma")}
        for i, (src, (need, tgt)) in enumerate(merges.items()):
            print(f" {i+1}. Fuse {need}x {src} ➔ 1x {tgt} (You own: {self.shadows[src]})")
        choice = input("Enter Merge Option Code (0 to Exit): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(merges):
            src = list(merges.keys())[int(choice)-1]
            need, tgt = merges[src]
            if self.shadows[src] >= need:
                self.shadows[src] -= need
                self.shadows[tgt] += 1
                self.log = f"🧬 Success! Your duplicates evolved into a high-tier [{tgt}] Shadow!"
            else: self.log = f"❌ Error: You need {need}x {src} to execute this mutation."

    def item_market(self):
        print(f"\n[🧪 POTION MARKET] Current Gold: {self.gold}G")
        pots = [("Small Mana Shard (+50 MP)", 100, 50), ("Medium Potion (+250 MP)", 400, 250), ("Monarch Core (+1000 MP)", 1500, 1000)]
        for i, (name, cost, _) in enumerate(pots):
            print(f" {i+1}. Buy {name} ➔ Price: {cost} Gold")
        choice = input("Enter Potion Item Number (0 to Exit): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(pots):
            name, cost, mp_gain = pots[int(choice)-1]
            if self.gold >= cost:
                self.gold -= cost
                self.mana += mp_gain
                self.log = f"✅ Consumed {name}! Gained +{mp_gain} Mana Points."
            else: self.log = "❌ Transaction Blocked: Insufficient dungeon gold drops."

    def dungeon_run(self):
        if self.floor == 0:
            self.floor = 1
            self.log = "🎯 Tutorial Gate Traversed! Loaded Floor 1 Combat Arena."
            return
        
        print(f"\n⚔️ [LOADING ARENA]: Entering Floor {self.floor} Boss Room Grid...")
        time.sleep(0.4)
        
        # Core Dodge Check Logic Roll
        if random.randint(1, 100) <= self.get_dodge() or random.random() > 0.35:
            # Win State Drops Wheel
            gold_drop = self.floor * 50 + random.randint(10, 50)
            xp_drop = self.floor * 60 + 20
            self.gold += gold_drop
            self.xp += xp_drop
            self.log = f"🏆 FLOOR {self.floor} CLEARED! Rewards Dropped: +{gold_drop} Gold, +{xp_drop} XP!"
            self.floor += 1
            self.sync_passive_xp()
        else:
            # Safe death loop execution parameter
            self.log = f"💀 COMBAT DEPLETION: You died on Floor {self.floor}! Retrying this exact layout level."

    def execute_tutorial_0(self):
        print("\n" + "═"*50 + "\n🏰 FLOOR 0: THE AWAKENING GROUND\n" + "═"*50)
        input(" -> Press [ENTER] to execute motor movement tests... ")
        input(" -> Press [ENTER] to test Left Shift agility dash speed... ")
        self.xp += 100
        self.sync_passive_xp()
        while self.stat_points > 0:
            self.show_dashboard()
            self.allocate_stats()
        self.mana += 10
        while self.shadows["Common"] == 0:
            print(f"\nMana Pool: {self.mana} MP")
            if input("Type '1' to open shop and buy your first shadow soldier: ").strip() == "1":
                self.shadow_shop()
        self.floor = 1
        self.log = "🎉 Tutorial Complete! Step into the gate to enter Floor 1."

    def start_engine(self):
        if self.floor == 0: self.execute_tutorial_0()
        while True:
            self.show_dashboard()
            print("Select your next tactical layout move option:")
            print(" 1. ⚔️ Enter Floor Combat | 2. 📊 Distribute Stat Points | 3. 🛒 Shadow Shop")
            print(" 4. 🧬 Evolve Shadow Units | 5. 🧪 Buy Mana Potions    | 0. Shut Down Game")
            action = input("Command Input Key: ").strip()
            if action == "1": self.dungeon_run()
            elif action == "2": self.allocate_stats()
            elif action == "3": self.shadow_shop()
            elif action == "4": self.merge_engine()
            elif action == "5": self.item_market()
            elif action == "0": print("\nClosing System interface profile. Goodbye, Monarch."); break

if __name__ == "__main__":
    SoloLevelingArcade().start_engine()
