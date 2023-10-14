from island import Island
from data_structures.bst import BinarySearchTree
from data_structures.bst import BSTInOrderIterator
from algorithms.mergesort import mergesort
from algorithms.binary_search import binary_search

class Mode1Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117


    The Mode1Navigator class employs a Binary Search Tree (BST) data structure for this purpose. 
    The complexity analysis is as follows:
    
    Initialization (init): The complexity is O(nlogn) in the worst and best cases, where n is the number of islands. This is because each island needs to be inserted into the BST, resulting in n iterations through the islands, with each insertion taking O(logn) time.

    Select Islands: In the best case, this operation takes O(1) time when all the crew is assigned to the first island, breaking out of the loop early. In the worst case, it takes O(n) time when all islands need to be considered. This operation involves traversing the entire BST.

    Update Island: Both the best and worst cases for updating an island are O(logn), as it requires searching for the specific island node within the BST. 

    Select Islands from Crew Numbers: In the 1008 version, the worst case is O(C * N), where C is the number of crew members, and N is the number of islands. It occurs when the entire tree is traversed for each crew number. In the 1054 version, the worst case is O(N + ClogC), as it traverses the tree once and sorts the crew numbers with a complexity of ClogC.

    In summary, the algorithm's overall time complexity mainly depends on the operations performed with the BST. Initialization and selecting islands can be time-consuming, especially when all islands need to be considered. Updating islands and selecting islands based on crew numbers have more predictable and efficient complexities.
        

    """

    def __init__(self, islands: list[Island], crew: int) -> None:
        """
        Student-TODO: Best/Worst Case

        :complexity:
            Best / worst case: O(nlogn)
                - n is the number of islands
                - occurs when we have to insert all the islands into the tree
        """
        
        self.island_tree = BinarySearchTree() 
        self.crew = crew



        for island in islands:
            # key is the ratio of marines to money
                # This is because we want to attack the island that will give us the most money per marine
                # so these islands will be at the left of the tree when using in order traversal
                    # larger ratio = less money per marine
            self.island_tree[island.marines / island.money] = island

    def select_islands(self) -> list[tuple[Island, int]]:
        """
        Select islands to attack 
        Return a list of tuples with the Island and the amount of crewmates you are sending

        Student-TODO: Best/Worst Case

        :complexity: 
            Best Case: O(1)
                - Occurs when when we send all crew members to the first island
                    - Break out of the loop after the first iteration
            Worst Case: O(n)
                - n is the number of islands 
                - occurs when we have to traverse the entire tree

 
        """
        selected_islands = []

        # copy crew to a variable so we can decrement it
            # according to crew spec we dont want to modify the original crew value
        crew = self.crew
        # Create an in order iterator to traverse the tree
            # this is so its sorted from smallest to largest ratio

        iterator = BSTInOrderIterator(self.island_tree.root)

        while crew > 0:
            try:
                # get the next node in the tree
                node = next(iterator)
                island = node.item
                marines = island.marines

                # if there are more marines than crew, send all the crew
                crew_sent = min(marines, crew)
                selected_islands.append((island, crew_sent))
                crew -= crew_sent
            except StopIteration:
                break

        return selected_islands


        
    def select_islands_from_crew_numbers(self, crew_numbers: list[int]) -> list[float]:
        """
        Calculate the most amount of money you can make with the given crew size
        Return a list of the amount of money you can make with the given crew size

        Student-TODO: Best/Worst Case

        :complexity:
            1008 version:
                Best / worst: O(C * N)
            1054 version:
                Best / worst: O(N + ClogC)
        """


        ###################### 1008 version ############################
        # N * C complexity
        # results = []
        # for crew in crew_numbers:
        #     self.crew = crew 
        #     total_money = 0
        #     for island, crew_sent in self.select_islands():
        #         total_money += island.money * crew_sent / island.marines
        #     results.append(total_money)
        # return results



        ###################### 1054 version ############################
        
        money_made = [0] * len(crew_numbers)

        # Original index, crew number
        sorted_crew = [(i, crew) for i, crew in enumerate(crew_numbers)]
        # Sort the crew numbers
        sorted_crew = mergesort(sorted_crew, key=lambda x: x[1])

        iterator = BSTInOrderIterator(self.island_tree.root) 

        # Variable to keep track of the current island
        node = next(iterator)
        island = node.item
        marines = island.marines
        money = island.money

        # Iterate through the sorted crew numbers
        for i, item in enumerate(sorted_crew):
            # get the original index and crew number
            og_index, crew = item

            # Use the previous money made so we dont have to recalculate
            if i>0:
                money_made[i] = money_made[i-1]
                crew -= sorted_crew[i-1][1]

            # Iterate through the islands
            while crew > 0:

                # Here we send marines to the island
                try:
                    crew_sent = min(marines, crew)
                    money_made[i] += money * crew_sent / island.marines
                    crew -= crew_sent
                    marines -= crew_sent
                    
                    # If there are no more marines, go to the next island
                    if marines == 0:
                        node = next(iterator)
                        island = node.item
                        marines = island.marines
                        money = island.money
                except StopIteration:
                    break


        
        og_order_money_made = [0] * len(crew_numbers)
        # put the money made back into the original order
            # match the index of each tuple to the original index
        for i, item in enumerate(sorted_crew):
            og_index, crew = item
            og_order_money_made[og_index] = money_made[i]
        
        return og_order_money_made




    

    def update_island(self, island: Island, new_money: float, new_marines: int) -> None:
        """
        Update the island with the new money and marines

        Student-TODO: Best/Worst Case

        :complexity:
            Best / worst: O(logn)
                - n is the number of islands
                - occurs when we have to search for the node to update
        """
        
        island.money = new_money
        island.marines = new_marines

if __name__ == "__main__":
    # islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    # nav = Mode1Navigator(islands, 200)
    # results = nav.select_islands_from_crew_numbers([0, 200, 500, 300, 40])
    # for i in results:
    #     print(i)
    
    print('\nTest Set 1. select_islands_from_crew_numbers()')
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    
    nav = Mode1Navigator(islands, 200)

    test_crew_numbers = [
        [0, 3, 4, 4],
        [0, 3, 4, 4, 5, 6, 7, 8, 9, 10],
        [0, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        [0, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        [0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        [9, 7, 2, 4, 2, 7, 9, 3, 100, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        [6999, 700, 1000000, 2, 3, 4, 6, 8, 1, 252524],
        [],
    ]

    expected = [
        [0.0, 60.0, 80.0, 80.0],
        [0.0, 60.0, 80.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0],
        [0.0, 60.0, 80.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, 124.0, 128.0],
        [0.0, 60.0, 80.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, 124.0, 128.0, 132.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 480.0, 0.0, 0.0, 0.0],
        [116.0, 108.0, 40.0, 80.0, 40.0, 108.0, 116.0, 60.0, 480.0, 80.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, 124.0, 128.0, 132.0], 
        [1450.0, 1450.0, 1450.0, 40.0, 60.0, 80.0, 104.0, 112.0, 20.0, 1450.0],
        [],
    ]

    for i in range(len(test_crew_numbers)):
        res = nav.select_islands_from_crew_numbers(test_crew_numbers[i])
        print(f"Test {i+1}:", "pass" if res == expected[i] else "fail")

    print('\nTest Set 2. select_islands()')
    
    ocean = [
        [Island(name='Dawn Island', money=463891799000, marines=198), Island(name='Zou', money=49973040500, marines=159), Island(name='Enies Lobby', money=229621144000, marines=261), Island(name='Sabaody Archipelago', money=1875319370500, marines=162), Island(name='Skypeia', money=398061434000, marines=264), Island(name='Whole Cake Island', money=1779576013000, marines=5), Island(name='Water 7Ohara', money=1625292916500, marines=280), Island(name='Little Garden', money=1547377772000, marines=227), Island(name='Jaya', money=172060744000, marines=255), Island(name='Dawn Island', money=1375255418000, marines=153)],
        [Island(name='Long Ring Long Land', money=453357110000, marines=98), Island(name='Zou', money=1734578774000, marines=204), Island(name='Fish-Man Island', money=1905620583000, marines=183), Island(name='Jaya', money=963313466000, marines=19), Island(name='Water 7Ohara', money=1215311237500, marines=247), Island(name='Dressrosa', money=818944371500, marines=176), Island(name='Loguetown', money=1761861698500, marines=168), Island(name='Drum Island', money=703352173500, marines=162), Island(name='Wano Country', money=897570512500, marines=57), Island(name='Fish-Man Island', money=753472893000, marines=2)],
        [Island(name='Thriller Bark', money=968629852000, marines=178), Island(name='Gecko Islands', money=1326699602500, marines=278), Island(name='Zou', money=844493283500, marines=16), Island(name='Enies Lobby', money=566637240000, marines=164), Island(name='Cactus Island', money=746935278500, marines=179), Island(name='Thriller Bark', money=858159047500, marines=94), Island(name='Cactus Island', money=651464229500, marines=35), Island(name='Punk Hazard', money=1956877887000, marines=123), Island(name='Shimotsuki Village', money=230363344500, marines=243), Island(name='Arabasta Kingdom', money=751432838500, marines=104)],
        [Island(name='Cactus Island', money=2121731340500, marines=250), Island(name='Skypeia', money=1894681033000, marines=225), Island(name='Thriller Bark', money=1462055850500, marines=89), Island(name='Dawn Island', money=1352620981000, marines=22), Island(name='Wano Country', money=580644676000, marines=257), Island(name='Dawn Island', money=1151971893000, marines=106), Island(name='Skypeia', money=1327578209500, marines=101), Island(name='Gecko Islands', money=943988690000, marines=210), Island(name='Zou', money=593785387500, marines=38), Island(name='Baratie', money=309212017500, marines=245)] ,
        [Island(name='Gecko Islands', money=682116009500, marines=181), Island(name='Shimotsuki Village', money=658280893500, marines=182), Island(name='Baratie', money=1195286721500, marines=231), Island(name='Little Garden', money=1135931623500, marines=46), Island(name='Jaya', money=1142950132500, marines=250), Island(name='Skypeia', money=1097665709000, marines=85), Island(name='Impel Down', money=1695109204500, marines=280), Island(name='Water 7Ohara', money=1664376713000, marines=103), Island(name='Gecko Islands', money=7791885000, marines=195), Island(name='Loguetown', money=1044979577500, marines=296)]
    ]

    res = []
    for islands in ocean:
        m = Mode1Navigator(islands, 100)
        for island, sent in  m.select_islands():
            res.append((island.name, sent))

    
    expected = [('Whole Cake Island', 5), ('Sabaody Archipelago', 95), ('Fish-Man Island', 2), ('Jaya', 19), ('Wano Country', 57), ('Loguetown', 22), ('Zou', 16), ('Cactus Island', 35), ('Punk Hazard', 49), ('Dawn Island', 22), ('Thriller Bark', 78), ('Little Garden', 46), ('Water 7Ohara', 54)]
    print(f"Test 1: ", "pass" if res == expected else "fail")

    print('\nTest Set 3. update_island()')
    original_islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    islands = [Island("A", 400, 100), Island("B", 300, 150), Island("C", 100, 5), Island("D", 350, 90), Island("E", 300, 100)]
    
    nav = Mode1Navigator(islands, 200)
    for island in islands:
        nav.update_island(island, island.money, island.marines)
    for island in islands:
        nav.update_island(island, island.money-1, island.marines-1)

    for index, island in enumerate(islands):
        print(f"Test {index+1}: ", "pass" if island.money == original_islands[index].money-1 and island.marines == original_islands[index].marines-1 else "fail")

    print()
