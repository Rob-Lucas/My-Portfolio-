#Robert Lucas
#11/29/2021
#HasamiShogiGame.py Allows one to play a game of HasamiShogi. Really frustrated with this and wanted to complete it but I have 4 major projects due by today and don't have enough time. If you comment out the get_capture function the code will run.
#This was one of the first things I wrote in python so it is a bit of a mess.

class HasamiShogiGame():
    """
    Allows one to play a game of Hasami Shogi Game
    Accessable Methods:
    get_game_state
    get_active_player
    get_num_captured_pieces
    set_num_captured_pieces
    set_turn_state
    set_position
    make_move
    get_win
    get_square_occupant
    get_capture
    new_game
    get_board_setup
    remove_pieces
    get_location
    get_location_reverse
    """
    def __init__(self):
        self._turn_state = 0
        self._Red = 0
        self._Blk = 0
        self._listoflist = [[""]]  
        self._alphabet = "abcdefghi"
        self._numbers = "123456789"
        self.new_game()

    def get_game_state(self):
        """
        Tells current state of game.Takes no parameters
        and determines if game is UNFINISHED or who the
        winner of the game is. If game state is won,
        self._turn_state will be 3 or 4. 3 is BLK while
        4 is Red. 
        """
        state=0
        if self._turn_state==0 or 1 or 2:
            state="UNFINISHED"
        elif self._turn_state==3:
            state="BLACK_WON"
        elif self._turn_state==4:
            state="RED_WON"
        return state

    def get_active_player(self):
        """
        Takes no parameters. Returns who's turn it is.
        Turns will be organized with self._turn_state 
        becoming a 2 for Red, and a 1 for Black. If turn 
        state is equal to 0, by game rules Black goes first.
        """
        check = self._turn_state
        if check == 0:
            state= "BLACK"
        elif check == 1:
            state= "BLACK"
        elif check==2:
            state= "RED"
        else:
            state= "GAME_OVER"
        return state

    def get_num_captured_pieces(self,player):
        """
        Determines the amount of captures pieces that a 
        player has. Requires the player as a parameter.
        This is calculated by taking the color and matching
        it to the self._Color of choice. That variable is 
        set with set command set_num_captured_pieces.
        Returns players number of pieces.
        """
        if player=="BLACK":
            return self._Blk
        elif player=="RED":
            return self._Red
        else:
            return "INVALID_PLAYER"

    def set_num_captured_pieces(self,player):
        """
        Set command used to count the number of pieces 
        captured. Takes in the player as a parameter.
        This is done by adding to the amount of self._Red
        or self._BLK. If game is over, sets the number to 0.
        """
        if player == 0:
            self._Blk +=1
        elif player == 1:
            self._Red +=1
        else:
            return "INVALID_CHARACTER"

    def set_turn_state(self,win):
        """
        Every time a play is conducted, sets the turn
        state to the next player. If one player wins,
        the parameter is set to that player. 3=BLK, 4=RED.
        If win = 1 or 2 then it simply sets the self._turn_state
        to the corresponding players turn. 1 = Black, 2 = Reds turn.
        """
        if win == 1:
            self._turn_state = 1
        elif win == 2:
            self._turn_state = 2
        elif win == 3:
            self._turn_state = 3
        elif win == 4:
            self._turn_state = 4
        pass

    def set_position(self,start, end):
        """
        Takes two parameters which is the desired postion
        and the start position. Takes the information and
        sets the pieces position to the desired position.
        This is a helper function to make_move. This 
        method then pushes the end position to get_capture
        to determine if you captured any pieces.
        """
        start_loc = self.get_location(start)
        end_loc = self.get_location(end)
        self._listoflist[start_loc[0]][start_loc[1]]="."
        player = self.get_active_player()
        self._listoflist[end_loc[0]][end_loc[1]]=player[0]
        if self._turn_state == 0:
            self._turn_state = 2
        elif self._turn_state == 1:
            self._turn_state = 2
        elif self._turn_state == 2:
            self._turn_state = 1
        self.get_capture(end)

    def make_move(self,start,end):
        """
        Takes two parameters, the current squares string,
        and the string for the square that you want.
        Uses get_game_state to determine whos turn it is. 
        Returns False if turn is not yours, if move is
        not legal, or if game over (done by future tests). Uses get_square_occupant
        for if the movement is legal. Checks if game is over by 
        checking self._turn_state which also determines
        if make_move returns False or not. Afterwards, determines
        if there are any pieces in the way of the desired path and returns False
        if that is an illegal move. Once everything is completed, 
        the function coordinates to the set_position method
        to place the piece in that position.
        """
        color_occu1= self.get_square_occupant(start)
        color_occu2= self.get_square_occupant(end)
        color_state= self.get_active_player()
        if color_state != color_occu1:
            return False
        if color_occu2 != None:
            return False
        if start[0] != end[0]:
            if start[1] != end[1]:
                return False
        beginning = self.get_location(start)
        ending = self.get_location(end)
        counter2=0
        if start[0] == end[0]:
            if ending[1] > beginning[1]:
                counter2 = beginning[1] +1
                while counter2 < ending[1]:
                    position = self.get_location_reverse(beginning[0], counter2)
                    if self.get_square_occupant(position) != None:
                        return False
                    else:
                        counter2+=1
            else:
                counter2=ending[1] +1
                while counter2 < beginning[1]:
                    position = self.get_location_reverse(beginning[0], counter2)
                    if self.get_square_occupant(position) != None:
                        return False
                    else:
                        counter2+=1
        elif start[1] == end[1]:
            if ending[0] > beginning[0]:
                counter2 = beginning[0] +1
                while counter2 < ending[0]:
                    position = self.get_location_reverse(counter2, beginning[1])
                    if self.get_square_occupant(position) != None:
                        return False
                    else:
                        counter2+=1
            else:
                counter2=ending[0] +1
                while counter2 < beginning[0]:
                    position = self.get_location_reverse(counter2,beginning[1])
                    if self.get_square_occupant(position) != None:
                        return False
                    else:
                        counter2+=1
        self.set_position(start, end)

    def get_win(self):
        """
        Takes in no parameters. This program is ran 
        to determine if a player won after their turn.
        """
        if self._Blk == 8:
            self._turn_state = 3
        elif self._Red == 8:
            self._turn_state = 4
        else:
            return

    def get_location(self,location):
        """
        Gets the x and y coordinates for position in
        the list of lists. Takes in one parameter which
        is the position that is desired to be broken down.
        """
        row=0
        column=0
        for i in range(len(self._listoflist)):
            if location[0] == self._listoflist[i][0]:
                row=i
                for i in range(len(self._listoflist)):
                    if location[1] == self._listoflist[0][i]:
                        column=i
        # print(row)    #For testing
        # print(column)
        return (row,column)

    def get_location_reverse(self,x,y):
        """
        Takes an x and y coordinate an tells what is 
        in that square.
        """
        location1=self._listoflist[x][0]
        location2=self._listoflist[0][y]
        location = location1+location2
        return location

    def get_square_occupant(self,location):
        """
        Tells if the square is occupied and by who. Requires
        a parameter for the squares location. Returns BLACK,
        RED, or NONE. To do this, the method calls position 0 and
        1 of the string, then checks each list for its 
        corresponding letter, and then uses a for loop to the 
        list the number of times that it was required to get to
        the position in that row. Afterwards, uses the positions
        (number in sequence) to find what is in that location.
        Will return an Error if game has not started yet.
        """
        check_location = self.get_location(location)
        row=check_location[0]
        column=check_location[1]
        if self._listoflist[row][column] == ".":
            return None
        elif self._listoflist[row][column] == "B":
            return "BLACK"
        elif self._listoflist[row][column] == "R":
            return "RED"
        else:
            return "ERROR"


    def get_capture(self, position):
        """
        This method uses parameters which is the location
        that someone wants to move to. Afterwards, checks all
        surrounding positions and determines if a piece is nearby
        of a different color. If there is, it continues that direction
        until it either finds an allied piece, or an empty location. 
        The code is designed to run even without this method to allow
        better testing. If pieces are to be captured, the locations are
        saved and the remove_pieces method is ran.
        """
        location = self.get_location(position)
        location2= self.get_location(position)
        player = self.get_square_occupant(position)
        up = location[1] - 1
        down = location[1] + 1
        left = location[0] - 1
        right = location[0] + 1
        checker = [up,down,left,right]
        count = 0
        for i in checker:
            enemy_positions=[]
            current = i
            corner_check = [1,9]
            num = 0
            if i is up or down:
                num = self.get_location_reverse(location[0],i)
            else:
                num = self.get_location_reverse(i,location[1])
            while self.get_square_occupant(location2) != None:
                if self.get_square_occupant(num) == "RED":
                    if player == "Black":
                        enemy_positions.append(num)
                        if current == up:
                            num = self.get_location_reverse(location2[0],location2[1]-1) 
                        elif current == down:
                            num = self.get_location_reverse(location2[0],location2[1]+1) 
                        elif current == left:
                            num = self.get_location_reverse(location2[0]-1,location2[1])
                        elif current == right:
                            num = self.get_location_reverse(location2[0]+1,location2[1])                   
                elif self.get_square_occupant(num) == "BLACK":
                    if player == "RED":
                        enemy_positions.append(num)
                        if current == up:
                            num = self.get_location_reverse(location2[0],location2[1]-1) 
                        elif current == down:
                            num = self.get_location_reverse(location2[0],location2[1]+1) 
                        elif current == left:
                            num = self.get_location_reverse(location2[0]-1,location2[1])
                        elif current == right:
                            num = self.get_location_reverse(location2[0]+1,location2[1])   
                location2=self.get_location(num)
                if self.get_square_occupant(num) == player:
                    if count > 0:
                        self.remove_pieces(enemy_positions,player)
                if count == 1:
                    if self.get_square_occupant(num) != player:
                        area = self.get_location(num)
                        if area[0] and area[1] in corner_check:
                            if num == "a1":
                                pos1 = self.get_square_occupant("a2")
                                pos2 = self.get_square_occupant("b1")
                                if pos1 and pos2 == player:
                                    enemy_positions.append("a1")
                            elif num == "i1":
                                pos1 = self.get_square_occupant("i2")
                                pos2 = self.get_square_occupant("h1")
                                if pos1 and pos2 == player:
                                    enemy_positions.append("i1")  
                            elif num == "i9":
                                pos1 = self.get_square_occupant("i8")
                                pos2 = self.get_square_occupant("h9")
                                if pos1 and pos2 == player:
                                    enemy_positions.append("i9")    
                            elif num == "a9":
                                pos1 = self.get_square_occupant("a8")
                                pos2 = self.get_square_occupant("b9")
                                if pos1 and pos2 == player:
                                    enemy_positions.append("a9") 
                            self.remove_pieces(enemy_positions,player)
                count += 1
            location2=location


    def remove_pieces(self,positions,player):
        """
        Takes in a list of positions from get_capture and who just went and 
        removes the pieces from those positions.
        """
        for i in range(len(positions)):
            if player == "BLACK":
                self.set_num_captured_pieces(0)
            if player == "RED":
                self.set_num_captured_pieces(1)
            placement = self.get_location(i)
            self._listoflist[placement[0]][placement[1]] = "."
        
        

    def new_game(self):
        """
        This method is for testing and for if you want to play 
        a new game. Uses set_current_state and plugs in win parameter
        as 0. 
        """
        self._turn_state = 0
        self._Red = 0
        self._Blk = 0
        self._listoflist = [[""]]
        counter=0
        for i in self._alphabet:
            self._listoflist.append([i])
        for i in self._numbers:
            self._listoflist[0].append(i)
        while counter < 9:
            counter+=1
            for i in self._numbers:
                if counter==1:
                    self._listoflist[counter].append("B")
                elif counter==9:
                    self._listoflist[counter].append("R")
                else:
                    self._listoflist[counter].append(".")            
        return self._listoflist

    def get_board_setup(self):
        """
        Prints a layout of the board in an easy to understand way.
        """
        for a,b,c,d,e,f,g,h,i,j in zip(*self._listoflist):
            print(a,b,c,d,e,f,g,h,i,j)
        print(self._listoflist)




lame= HasamiShogiGame()
lame.make_move("a1","f1")
lame.make_move("i2","f2")
# lame.make_move("a3","f3")
# lame.make_move("f2","f1")
# lame.make_move("f9","f2")
print(lame.get_active_player())
print(lame.get_square_occupant('f2'))
print(lame.get_game_state())
lame.get_board_setup()
