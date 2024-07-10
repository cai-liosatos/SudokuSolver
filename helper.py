import pygame as pg

def update_puzzle(grid, surface):
    surface.fill((pg.Color("white")))
    pg.draw.rect(surface, pg.Color("black"), pg.Rect(15, 15, 720, 720), 8)
    i = 1
    while (i*80) < 720:
        line_width = 5 if i % 3 > 0 else 8

        # vector, i*80 = iterator moving with while iterator, 15 is accounting for margins specified above, second 15 is accounting for y margins (top/bot)
        pg.draw.line(surface, pg.Color("black"), pg.Vector2((i*80)+15, 15), pg.Vector2((i*80)+15, 734), line_width)
        pg.draw.line(surface, pg.Color("black"), pg.Vector2(15, (i*80)+15), pg.Vector2(734, (i*80)+15), line_width)
        i += 1
        
    #draw in numbers from grid
    for i in range(0, 9):
        for j in range(0, 9):
            if isinstance(grid[i][j], list):
                formatted_list = sorted(grid[i][j])
                font = pg.font.Font(None, 30)
                grouped_value = [formatted_list[x:x+3] for x in range(0, len(formatted_list), 3)]
                for v in range(len(grouped_value)):
                    end_value = ', '.join(map(str, grouped_value[v]))
                    value = font.render(str(end_value), True, pg.Color("black"))
                    string_width = value.get_width()
                    string_height = value.get_height()
                    intended_height = 50-(((len(grouped_value)-1)*(string_height/2)))+(string_height*v)
                    surface.blit(value, ((j)*80 + (56-(string_width/2)), (i)*80 + intended_height))
            else:
                if (0<grid[i][j]<10):
                    font = pg.font.Font(None, 72)
                    value = font.render(str(grid[i][j]), True, pg.Color("black"))
                    value_height = value.get_height()
                    surface.blit(value, ((j)*80 + 40, (i)*80 + 40))

            