# ==============================================================================
"""PolyMaze Maze Rendering"""
# ==============================================================================
__author__  = "Lemaire Pierre & Rawat Eshane"
__version__ = "Maze rendering 1.1"
__date__    = "2015-03-30"
# =======================================================

import Mazegen
from PIL import Image, ImageOps, ImageChops

class maze_rendering(Mazegen.maze_generator):
    def __init__(self):
        Mazegen.maze_generator.__init__(self)
        #Basic img dimension to be used. 
        self.imgW = 512
        self.imgH = 512

    def render_maze2D(self):
        #simple method using pillow lib and carve_maze to "draw" the maze
        image = Image.new("RGB", (self.imgW, self.imgH))
        pix = image.load()
        maze = self.new_maze(0,0)
        #cell building, white if path, black if wall
        for cy in range(self.imgH):
            for cx in range(self.imgW):
                if self.maze[self.width * cy // self.imgH][self.height * cx // self.imgW] == 0:
                    pix[cx, cy] = (0, 0, 0)
                else:
                    pix[cx, cy] = (255,255,255)
        #starting point
        for sy in range(11):
            for sx in range(11):
                pix[sy, sx] = (0, 255, 0)
        #ending of the maze
        for ey in range(502,512):
            for ex in range(502,512):
                pix[ey, ex] = (0, 0, 255)
        #adds a border to the image to close the maze
        rendered = ImageOps.expand(image, border=2, fill='black')
        #print, to be removed later on
        rendered.show()
        return rendered.save("Maze.png", "PNG")

    def texture(self):#TODO --> affiner les textures pour que ça soit plus OP encore
        ground_tex = Image.open("ground-tex.png")
        ground_tex = ground_tex.convert('RGB')
        wall_tex = Image.open("wall-tex.png")
        wall_tex = wall_tex.convert('RGB')
        mask = Image.open("Maze.png")
        mask = mask.convert('RGB')

        #adds texture to the walls
        texture = ImageChops.add(mask,wall_tex)
        #Vertical symetry to fit the 3D model
        texture = ImageOps.flip(texture)
        #Print to be removed later on
        texture.show()
        return texture.save("texture.png", "PNG")

    def render_maze3D(self):
        self.texture()
        text = open('maze3D.obj','w')
        text.write('#obj file \n')
        twoD = Image.open("Maze.png")
        pix_twoD = twoD.load()
        self.imgW, self.imgH = twoD.size
        #vertex writing
        for y in range(self.imgH):
            for x in range(self.imgW):
                if pix_twoD[x,y] == (0,0,0):
                    z = 2
                    text.write("v "+str(50*x/self.imgW)+" "+str(50*y/self.imgH)+" "+str(z)+" \n")
                else:
                    z = 0
                    text.write("v "+str(50*x/self.imgW)+" "+str(50*y/self.imgH)+" "+str(z)+" \n")

        #texture writing
        for y in range(self.imgH):
            for x in range(self.imgW):
                text.write("vt "+str(x/self.imgW)+" "+str(y/self.imgH)+" \n")
        #call the mtl lib        
        text.write("mtllib textureA.mtl \nusemtl texture \n")

        #face writing
        for y in range(self.imgH-1):
            for x in range(self.imgW-1):
                f1 = str((self.imgW*y)+1+x)
                f2 = str((self.imgW*y)+2+x)
                f3 = str((self.imgW*(y+1))+2+x)
                f4 = str((self.imgW*(y+1))+1+x)
                text.write("f "+f1+"/"+f1+" "+f2+"/"+f2+" "+f3+"/"+f3+" "+f4+"/"+f4+" \n")


def main():
    d = maze_rendering()
    d.render_maze2D()
    d.render_maze3D()


if __name__ == "__main__" :
    main()


