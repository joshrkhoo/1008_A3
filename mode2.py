from island import Island
from data_structures.heap import MaxHeap


class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117

    Data Structures:
        - islands: list of islands
            - A list was used as it had O(1) access time to the islands and O(n) time to add islands
            - This allowed for the use of enumeration to keep track of the island index, avoiding the comparision between island objects when the score was the same
                - (score, index)
        - heap_islands: heap of islands
            - A MaxHeap was used as it served its main purpose of functioning as a priority queue
            - This was used to keep track of the islands with the highest score
            - It also made sense as the pirates would plunder the island with the highest score first
            - Using a different data structure would have resulted in a higher time complexity
        
    Time Complexity:
        Initialisation:
            - O(1)
            - Constant operations are used
        add_islands:
            - O(n)
                - n is the number of islands
            - Iterate through the list of islands and add them to the sea
        create_heap_islands:   
            - O(n)  
                - n is the number of islands
            - This is beacuse heapify is O(n) and the iteration is O(n)
                so the total time complexity is O(n + n) = O(2n) = O(n)
        money_made:
            - O(1)
            - Constant operations are used
        calculate_score:
            - O(1)
            - Constant operations are used
        update_island:  
            - O(1)
            - Constant operations are used
        update_heap_islands:
            - O(1)
                - This would occur when no need to rise
            - O(logn)
                - n is the number of islands
            - This is because add uses the rise function which is O(logn)
        choose_action:
            - O(logn)
                - n is the number of islands
            - This is because get_max is O(logn) due to sink
        simulate_day:
            - O(n + clogn)
                - n is the number of islands
                - c is the number of pirates
                - This occurs due to the following reasons:
                    - creation of sea is O(n)
                    - for loop is O(c)
                    - choose_action is O(logn) always due to get_max


    """

    def __init__(self, n_pirates: int) -> None:
        """
        Initialises a new navigator with the given number of pirates.

        :complexity: 
            Best/Worst: O(1)
        """
        
        self.n_pirates = n_pirates
        self.islands = []
        self.heap_islands = None

    def add_islands(self, islands: list[Island]) -> None:
        """
        Adds the given islands to the sea

        :complexity:
            Best/Worst: O(n)
                - n is the number of islands
        """
        for island in islands:
            self.islands.append(island)

    def create_heap_islands(self, islands: list[Island], crew: int) -> None:
        """
        Creates a heap of islands based on the score of each island

        :complexity:
            Best/Worst: O(n)
                - n is the number of islands
                - calculate_score is O(1)
                - heapify is O(n) 
                    - O(n + n) = O(2n) = O(n)

        """

        new_islands = []

        for num, island in enumerate(islands):
            score = self.calculate_score(crew, island)
            new_islands.append((score, num))
        
        # print(new_islands)

        return MaxHeap.heapify(new_islands)


    
    def money_made(self, island: Island, crew: int) -> int:
        """
        Calculates the money made from plundering an island

        :complexity:
            Best/Worst: O(1)
        """
        if island.marines == 0:
            return island.money
        return min(island.money, island.money * crew / island.marines)
    

    
    def calculate_score(self, crew: int, island: Island) -> int:
        """
        Calculates the score of an island

        :complexity:
            Best/Worst: O(1)
        """
        crew_sent = min(island.marines, crew)
        crew_remaining = crew - crew_sent
        money_made = self.money_made(island, crew_sent)
        score = 2 * crew_remaining + money_made
        return score
    


    def update_island(self, island: Island, crew: int) -> None:
        """
        Updates the island after plundering

        :complexity:
            Best/Worst: O(1)
        """
        island.money -= self.money_made(island, crew)
        island.marines -= crew

    
    def update_heap_islands(self, island_index, crew: int) -> None:
        """
        Updates the sea/heap of islands after plundering

        :complexity:
            Best case: O(1)
                - no need to rise
            Worst case: O(logn)
                - n is the number of islands
                - add is O(1)
                - rise is O(logn)
        """

        if self.islands[island_index].money > 0:
            updated_score = self.calculate_score(crew, self.islands[island_index])
            self.heap_islands.add((updated_score, island_index))
        


    def choose_action(self, crew: int, sea) -> tuple[Island, int]:
        """
        Chooses the best action to take

        :complexity:
            Best/Worst: O(log n)
                - n is the number of islands
                - get_max is O(log n) due to sink
                - calculate_score is O(1)
                - add is O(1)
        """

        if_skip = 2 * crew
        score, island_index = sea.get_max()
        crew_sent = min(self.islands[island_index].marines, crew)

        if score <= if_skip:
            action = (None, 0)
        else:
            action = (island_index, crew_sent)

        return action
        

 

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Simulates a day of plundering

        :complexity:
            Best/Worst: O(n + clogn)
                - n is the number of islands
                - c is the number of pirates
                - This occurs due to the following reasons:
                    - creation of sea is O(n)
                    - for loop is O(c)
                    - choose_action is O(logn) always due to get_max
        """
        
        # Create heap using new_islands list
        # O(n)
        self.heap_islands = self.create_heap_islands(self.islands, crew)


        results = []

        # O(c)
        for i in range(self.n_pirates):

            

            if len(self.heap_islands) > 0: 

                island_index, crew_sent = self.choose_action(crew, self.heap_islands)
                
                if crew_sent == 0:
                    results.append((None, 0))
                    continue

                results.append((self.islands[island_index], crew_sent))

                # Update island
                self.update_island(self.islands[island_index], crew_sent)

                # Add island back to heap
                self.update_heap_islands(island_index, crew)

            else:
                results.append((None, 0))            
        
        return results



if __name__ == "__main__":
    def check_islands_same(island1, island2):
        if island1 is None:
            return island2 is None
        return island1.name == island2.name and island1.money == island2.money and island1.marines == island2.marines

    def get_island_details(island):
        if island is None:
            return None, None, None
        return (island.name, island.money, island.marines)
        
    print("\nTest Set 1.")

    m2 = Mode2Navigator(1)
    islands = [Island("A", 400, 100)]
    m2.add_islands(islands)

    expected = [['A', 360.0, 90, 10], 
                ['A', 320.0, 80, 10], 
                ['A', 280.0, 70, 10], 
                ['A', 240.0, 60, 10], 
                ['A', 200.0, 50, 10], 
                ['A', 160.0, 40, 10], 
                ['A', 120.0, 30, 10], 
                ['A', 80.0, 20, 10], 
                ['A', 40.0, 10, 10], 
                ['A', 0.0, 0, 10], 
                [None, None, None, 0]
                ]
    for i in range(11):
        res = m2.simulate_day(10)
        name, money, marines = get_island_details(res[0][0])
        sent = res[0][1]

        print(f"Test {i+1}: ", "pass" if expected[i]==[name, money, marines, sent] else "fail")

    print("\nTest Set 2.")

    m2 = Mode2Navigator(10)
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    m2.add_islands(islands)

    expected = [[['C', 0, 0, 5], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10], ['A', 40.0, 10, 10]], 
                [['A', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10], ['D', 0.0, 0, 10]], 
                [['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10], ['E', 0.0, 0, 10]], 
                [[None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0]]]

    got = []
    for i in range(4):
        res = m2.simulate_day(10)
        
        line = []
        for island in res:
            name, money, marines = get_island_details(island[0])
            sent = island[1]
        
            line.append([name, money, marines, sent])

        got.append(line)

        # print(res)
        
    for i in range(4):
        print(f"Test {i+1}: ", "pass" if expected[i]==got[i] else "fail")


    print("\nTest Set 3.")

    new_islands = [Island("F", 100, 5), Island("G", 100, 20)]
    m2.add_islands(new_islands)
    expected = [[['F', 0.0, 0, 1], ['F', 0.0, 0, 1], ['F', 0.0, 0, 1], ['F', 0.0, 0, 1], ['F', 0.0, 0, 1], ['G', 75.0, 15, 1], ['G', 75.0, 15, 1], ['G', 75.0, 15, 1], ['G', 75.0, 15, 1], ['G', 75.0, 15, 1]], [['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1], ['G', 25.0, 5, 1]], [['G', 0.0, 0, 1], ['G', 0.0, 0, 1], ['G', 0.0, 0, 1], ['G', 0.0, 0, 1], ['G', 0.0, 0, 1], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0]], [[None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0], [None, None, None, 0]]]
    got = []
    for i in range(4):
        res = m2.simulate_day(1)
        
        line = []
        for island in res:
            name, money, marines = get_island_details(island[0])
            sent = island[1]
        
            line.append([name, money, marines, sent])

        got.append(line)

        # print(res)
    
    for i in range(4):
        print(f"Test {i+1}: ", "pass" if expected[i]==got[i] else "fail")

    print("\nTest Set 4.")
    m2 = Mode2Navigator(3)

    islands = [Island("A", 400, 100), Island("B", 300, 150)]
    more_islands = [Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
 
    m2.add_islands(islands)
    m2.add_islands(more_islands)

    res = []
    for island, sent_crew in m2.simulate_day(100):
        res.append((island.name, sent_crew))

    m2.add_islands([Island("F", 900, 150)])
    for island, sent_crew in m2.simulate_day(100):
        res.append((island.name, sent_crew))
    
    print("Test 1: ", "passed" if len(res)==6 else "failed")
    print("Test 2: ", "passed" if res == [('A', 100), ('D', 90), ('E', 100), ('F', 100), ('F', 50), ('C', 5)]  else "failed")

    print("\nTest Set 5.")

    m2 = Mode2Navigator(100)
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    for island in islands:
        m2.add_islands([island])
    res = m2.simulate_day(0)
    print("Test 1: ", "passed" if len(res) == 100 else "failed")
    passed = True
    for r in res:
        if r[0] != None:
            passed = False
        if r[1] != 0:
            passed = False
    print("Test 2: ", "passed" if passed else "failed")

    print("\nTest Set 6.")
    m2 = Mode2Navigator(100)
    res = m2.simulate_day(0)
    print("Test 1: ", "passed" if len(res) == 100 else "failed")
    passed = True
    if len(res) != 100:
        passed = False
    for r in res:
        if r[0] != None:
            passed = False
        if r[1] != 0:
            passed = False
    print("Test 2: ", "passed" if passed else "failed")


            

            

                