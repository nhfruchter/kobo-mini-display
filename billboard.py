import pygame
import os
import argparse
from subprocess import call

# Tell graphics engine there's no mouse
os.environ['SDL_NOMOUSE'] = '1'

def to_hex(color):
    ''' convert a colour value into a hexadecimal value 
    Based on Kevin Short's koboWeather app
    '''
    hex_chars = "0123456789ABCDEF"
    return hex_chars[color / 16] + hex_chars[color % 16]
    
def convert_to_raw(surface):
    ''' convert an SDS drawing surface into a raw image format.
    saves the raw data in /tmp/img.raw.
    Based on Kevin Short's koboWeather app
    '''
    print("Converting image . . .")
    raw_img = ""
    for row in range(surface.get_height()):
        for col in range(surface.get_width()):
            color = surface.get_at((col, row))[0]
            raw_img += ('\\x' + to_hex(color)).decode('string_escape')
    f = open("/tmp/img.raw", "wb")
    f.write(raw_img)
    f.close()
    print("Image converted.")
    
def text(string, font="sans", size=48, topleft=(10,15)):    
    FONTBASE = "fonts/"
    FONTS = {'sans': 'Fabrica.otf', 'serif': 'Forum-Regular.otf'}

    font = pygame.font.Font(FONTBASE+FONTS[font], size)
    text = font.render(string, True, (0,0,0), (255,255,255))
    rect = text.get_rect()
    rect.topleft = topleft
    
    return text, rect
    
def billboard(message, size=48, font="sans", landscape=False):
    print("Creating Image")

    # Screen properties
    ANGLE = 90 * (landscape + 1)
    DIMENSIONS = (800,600) if landscape else (600,800)

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (125, 125, 125)

    # Initialize PyGame
    pygame.display.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)
    display = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    screen = pygame.Surface(DIMENSIONS)
    screen.fill(white)
    
    # Draw text
    rendered = text(message, size=size, font=font)
    screen.blit(*rendered)
    
    # Render
    graphic = pygame.transform.rotate(screen, ANGLE)
    display.blit(graphic, (0, 0))    
    pygame.display.update()
    call(["/mnt/onboard/full_update"])
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Draw text on the Kobo screen.")
    parser.add_argument('-f', dest='font', help='Font to use (serif or sans; defaults to sans).', default='sans')
    parser.add_argument('-s', dest='size', help='Character size (defaults to 48).', type=int, default=48)
    parser.add_argument('--landscape', dest='landscape', help='Display in landscape.', action='store_true')
    parser.add_argument('message', type=str)
    
    args = parser.parse_args()
    
    billboard(args.message, size=args.size, font=args.font, landscape=args.landscape)
    