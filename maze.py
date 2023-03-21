import numpy as np
from PIL import Image, ImageDraw
images = []

#Read input

def readMaze(fileName):
    #read the text file
    maze = []
    with open(fileName, 'r') as f:
        for line in f:
            maze.append(list(line.strip()))
    return maze

#Check a cell is valid or not
def isValid(maze, row, col):
    return (row >= 0 and row < len(maze) and col >= 0 and col < len(maze[0]) and maze[row][col] != '#')

#Find the start
def findStart(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == '^':
                return r, c

#Find the exit
def findExit(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'E':
                return r, c

#Find the route
def solveMaze(maze, maxMoves):
    #check if the maze is valid
    if maze == None or len(maze) == 0 or len(maze[0]) == 0:
        return False
    #find the starting and exit positions
    startR, startC = findStart(maze)
    exitR, exitC = findExit(maze)
    #create a 2d array to store the solution path
    finalPath = [[-1 for i in range(len(maze[0]))] for j in range(len(maze))]
    #create a queue to store the nodes
    q = []
    q.append([startR, startC, 0])
    #loop until the queue is empty
    while len(q) > 0:
        currR, currC, moves = q.pop(0)
        #if the current cell is the exit
        if currR == exitR and currC == exitC:
            finalPath[currR][currC] = moves
            break
        #if the current cell is valid and not visited before
        if isValid(maze, currR, currC) and finalPath[currR][currC] == -1:
            #mark the cell as visited
            finalPath[currR][currC] = moves
            #add the adjacent cells to the queue
            if moves < maxMoves:
                q.append([currR + 1, currC, moves + 1])
                q.append([currR - 1, currC, moves + 1])
                q.append([currR, currC + 1, moves + 1])
                q.append([currR, currC - 1, moves + 1])
    #print the solution if the exit is found
    if finalPath[exitR][exitC] != -1:
        print(maxMoves,": yes")
        return True
    else:
        print(maxMoves,": No possible route")
        return False

# main function
if __name__ == "__main__":
    #read the maze
    fileName = input("Enter maze file name: ")
    file = open(fileName, "r")
    maze = readMaze(fileName)
   
    #solve the maze
    solveMaze(maze, 20)
    solveMaze(maze, 150)
    solveMaze(maze, 200)

  #create a visual representation of the maze
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == '#':
                image = Image.new("RGB", (20, 20), (255, 255, 255))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, 19, 19), fill=(0, 0, 0))
                images.append(image)
            elif maze[r][c] == '^':
                image = Image.new("RGB", (20, 20), (255, 255, 255))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, 19, 19), fill=(255, 0, 0))
                draw.rectangle((2, 2, 17, 17), fill=(0, 0, 0))
                images.append(image)
            elif maze[r][c] == 'E':
                image = Image.new("RGB", (20, 20), (255, 255, 255))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, 19, 19), fill=(0, 255, 0))
                draw.rectangle((2, 2, 17, 17), fill=(0, 0, 0))
                images.append(image)
            else:
                image = Image.new("RGB", (20, 20), (255, 255, 255))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, 19, 19), fill=(255, 255, 0))
                draw.rectangle((2, 2, 17, 17), fill=(0, 0, 0))
                images.append(image)
    #combine the images into one
    width = len(maze[0]) * 20
    height = len(maze) * 20
    result = Image.new("RGB", (width, height))
    x = 0
    y = 0
    for image in images:
        result.paste(image, (x, y))
        x += 20
        if x >= width:
            x = 0
            y += 20
    #save the image
    result.save("maze.png")