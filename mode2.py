from island import Island
from data_structures.heap import MaxHeap


class Mode2Navigator:
    """
    Student-TODO: short paragraph as per https://edstem.org/au/courses/12108/lessons/42810/slides/294117
    """

    def __init__(self, n_pirates: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        
        self.n_pirates = n_pirates
        self.islands = []

    def add_islands(self, islands: list[Island]) -> None:
        """

        add islands to seas

        Student-TODO: Best/Worst Case
        """
        for island in islands:
            self.islands.append(island)

    
    def money_made(self, island: Island, crew: int) -> int:
        """
        Student-TODO: Best/Worst Case
        """
        if island.marines == 0:
            return island.money
        return min(island.money, island.money * crew / island.marines)
        

    def simulate_day(self, crew: int) -> list[tuple[Island|None, int]]:
        """
        Student-TODO: Best/Worst Case

        1. Pirates get fresh crew
        2. Pirates take turns and have 2 options:
            - Plunder an island with a specific amount of crew
            - Do nothing
        3. Once all pirates have taken their turn, the day ends and the score is calculated
        4. Return a list of tuples containing the island plundered and the amount of crew sent
        5. Score is calculated as follows:
            - 2 x c + m
            - c = remaining crew
            - m = money plundered

        
        Other variables to consider
            - Island money and marines are altered after each plunder
                - if the island still has money and marines, it can be plundered again
                    - so we have to re add it to the heap
 
        worse case: O(N + Clog(N))
            - N is the number of islands w non zero money
            - C is the number of captains
        
        return a list of tuples containing the island plundered and the amount of crew sent


        make the heap of islands be score, island


        """
        new_islands = []

        # Calculate score for each island and add to new_islands
        for island in self.islands:
            crew_sent = min(island.marines, crew)
            crew_remaining = crew - crew_sent
            money_made = self.money_made(island, crew_sent)
            score = 2 * crew_remaining + money_made
            new_islands.append((score, island))
        
        # Create heap using new_islands list
        heap_islands = MaxHeap.heapify(new_islands)

        for number, tup in enumerate(heap_islands.the_array):
            print(number, tup) 


        results = []

        for i in range(self.n_pirates):
            crew_num = crew
            # Get island with highest score
            
            if len(heap_islands) == 0:
                results.append((None, 0))
                continue

            island = heap_islands.get_max()[1]
            
            crew_sent = min(island.marines, crew_num)

            # If more marines than crew
            if island.marines > crew_num:
                results.append((island, crew_sent))
                money_made = self.money_made(island, crew_sent)
                # Update island
                island.money -= money_made
                island.marines -= crew_sent
                # Add island back to heap
                heap_islands.add((island.money - money_made, island))

            # if more crew than marines or same
            else:
                results.append((island, crew_sent))
                money_made = self.money_made(island, crew_sent)
                # Update island
                island.money -= money_made
                island.marines -= crew_sent
        

        for number, tup in enumerate(results):
            print(number, tup)
        return results
                


                

                

                    