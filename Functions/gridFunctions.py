""" Necessary functions to use the Github Contributions Art"""
import matplotlib.pyplot as plt
import pandas as pd
import copy 
import os.path

import datetime as dt
import pandas as pd
from google.oauth2 import service_account
from datetime import datetime, timedelta
from pathlib import Path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



green_max  = "#196127"
green_more = "#239a3b"
green_less = "#7bc96f"
green_min  = "#c6e48b"


def set_background(theme): # fixes the background and empty boxes colors 
    if theme=='dark':
        box_edge_color = "#0d1117"      
        box_blank_color = "#161b22"      
        return box_edge_color, box_blank_color
    if theme=='light':
        box_edge_color = "#ffffff"      
        box_blank_color = "#eaecef"      
        return box_edge_color, box_blank_color
    else:
        print('theme should be set to "light" or "dark"')
        return None, None

def generate_dataframe(colors,box_blank_color): # generates a dataframe containing the schedual of contributions 

    unique_colors = [box_blank_color, green_min, green_less, green_more, green_max]


    # Create a mapping dictionary
    color_to_num = {color: (idx*2) for idx, color in enumerate(unique_colors)}

    # Convert the list of lists using the mapping
    numerical_matrix = [[color_to_num[color] for color in row] for row in colors]


    art_df = pd.DataFrame(numerical_matrix)

    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    weeks = ["W"+str(i+1) for i in range(53)]

    art_df.index = days
    art_df.columns = weeks
    return art_df

def create_grid(colors,box_edge_color): 
    grid_colors = copy.deepcopy(colors)
    rows, cols = len(grid_colors), len(grid_colors[0])
    n = 12
    fig, ax = plt.subplots(figsize=(n, n*7/53))  # Adjust size as needed

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    
    grid_colors[0][0] = box_edge_color
    grid_colors[1][0] = box_edge_color
    grid_colors[2][0] = box_edge_color
    grid_colors[3][52] = box_edge_color
    grid_colors[4][52] = box_edge_color
    grid_colors[5][52] = box_edge_color
    grid_colors[6][52] = box_edge_color
    
    

    
    # Draw each square
    for y in range(rows):
        for x in range(cols):
            color = grid_colors[y][x]
            ax.add_patch(plt.Rectangle((x, rows - 1 - y), 1, 1, 
                                        facecolor=color, edgecolor=box_edge_color))
            
    

    fig.patch.set_facecolor(box_edge_color)
    

    
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axis

    plt.savefig("grid_output.png", bbox_inches='tight')
    print(f"Grid saved as {"grid_output.png"}")

    return None




# --------------------------- ART num 1 ---------------------------

def create_line(colors, color, a0, b0, direction): 
    """
    color in hex
    a0 : starting column 
    b0 : starting row 
    direction : "up" or "down" 
    """

    match direction:
        case "up":
            for i in range(7):
                colors[a0-i][i+b0] = color
        case "down":
            for i in range(7):
                colors[i+a0][i+b0] = color



    return colors

def art_num1(colors, green_light, green_dark):

    green_max = green_dark
    green_more = green_light

    for col in range (7):
        residual = col%7
        match residual:
            case 0|4:
                colors = create_line(colors, green_more, 6,col, "up")
            case 1|2|3:
                colors = create_line(colors, green_max, 6,col, "up")
                
    for col in range (7):
        residual = col%7
        match residual:
            case 0|4:
                colors = create_line(colors, green_more, 0,col, "down")
            case 1|2|3:
                colors = create_line(colors, green_max, 0,col, "down")


    for col in range (7,14):
        residual = col%7
        match residual:
            case 1|2|3:
                colors = create_line(colors, green_max, 6,col+3, "up")
            case 0|4:
                colors = create_line(colors, green_more, 6,col+3, "up")

    for col in range (7,14):
        residual = col%7
        match residual:
            case 0|4:
                colors = create_line(colors, green_more, 0,col+3, "down")
            case 1|2|3:
                colors = create_line(colors, green_max, 0,col+3, "down")


    for col in range (14,21):
        residual = col%7
        match residual:
            case 1|2|3:
                colors = create_line(colors, green_max, 6,col+6, "up")
            case 0|4:
                colors = create_line(colors, green_more, 6,col+6, "up")

    for col in range (14,21):
        residual = col%7
        match residual:
            case 0|4:
                colors = create_line(colors, green_more, 0,col+6, "down")
            case 1|2|3:
                colors = create_line(colors, green_max, 0,col+6, "down")


    for col in range (21,28):
        residual = col%7
        match residual:
            case 1|2|3:
                colors = create_line(colors, green_max, 6,col+9, "up")
            case 0|4:
                colors = create_line(colors, green_more, 6,col+9, "up")

    for col in range (21,28):
        residual = col%7
        match residual:
            case 0|4:
                colors = create_line(colors, green_more, 0,col+9, "down")
            case 1|2|3:
                colors = create_line(colors, green_max, 0,col+9, "down")


    index = 10
    colors[0][index] = green_max
    colors[6][index] = green_max
    colors[1][index] = green_more
    colors[5][index] = green_more


    index = 20
    colors[0][index] = green_max
    colors[6][index] = green_max
    colors[1][index] = green_more
    colors[5][index] = green_more

    index = 30
    colors[0][index] = green_max
    colors[6][index] = green_max
    colors[1][index] = green_more
    colors[5][index] = green_more

    nn=4

    index = 44-nn
    colors[3][index] = green_max
    index = 45-nn
    colors[2][index] = green_max
    colors[4][index] = green_max
    index = 46-nn
    colors[1][index] = green_max
    colors[3][index] = green_more
    colors[5][index] = green_max
    index = 47-nn
    colors[0][index] = green_max
    colors[2][index] = green_more
    colors[3][index] = green_max
    colors[4][index] = green_more
    colors[6][index] = green_max
    index = 48-nn
    colors[1][index] = green_max
    colors[3][index] = green_more
    colors[5][index] = green_max
    index = 49-nn
    colors[2][index] = green_max
    colors[4][index] = green_max
    index = 50-nn
    colors[3][index] = green_max



    for col in range (28,35):
        residual = col%7
        match residual:
            case 4:
                colors = create_line(colors, green_more, 6,col+14, "up")

    for col in range (28,35):
        residual = col%7
        match residual:
            case 4:
                colors = create_line(colors, green_more, 0,col+14, "down")

    return colors

