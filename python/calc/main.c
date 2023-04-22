#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <pthread.h>
#include <sys/timeb.h>

#define SDL_MAIN_HANDLED
#include <SDL.h>




#define WIN_WIDTH  700
#define WIN_HEIGHT 700

int AREA = WIN_WIDTH * WIN_HEIGHT;
int YOFF = WIN_HEIGHT/2;
int XOFF = WIN_WIDTH/2;

float ASPECTRATIO = WIN_WIDTH/WIN_HEIGHT;

float yaw = 0;
float roll = 0;
float pitch = 0;

// temps
float a;
float b;
float c;
float d;
float e;
float f;
float g;
float h;
float i;

typedef struct {
    float x;
    float y;
    float z;

}SPOINT;

pthread_t pthread1;
pthread_t pthread2;
pthread_t pthread3;
pthread_t pthread4;

int main(int argc, char **argv) {

    //pthread_create(&pthread1, NULL, ca)

    // SDL init
    SDL_Init(SDL_INIT_VIDEO);

    // create SDL window
    SDL_Window *window = SDL_CreateWindow("idiot",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        WIN_WIDTH * 1,
        WIN_HEIGHT * 1,
        SDL_WINDOW_OPENGL/*SDL_WINDOW_FULLSCREEN_DESKTOP*/);

    SDL_SetWindowSize(window, 1000, 1000);

    // create renderer
    SDL_Renderer *renderer = SDL_CreateRenderer(
        window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    
    SDL_RenderSetLogicalSize(renderer, WIN_WIDTH, WIN_HEIGHT);

    // create texture
    SDL_Texture *texture = SDL_CreateTexture(
        renderer,
        SDL_PIXELFORMAT_RGBA32,
        SDL_TEXTUREACCESS_STREAMING,
        WIN_WIDTH,
        WIN_HEIGHT);



    // array of pixels
    

    uint8_t pixels[WIN_WIDTH * WIN_HEIGHT * 4] = {0};
    
    // original points
    SPOINT* points = malloc(sizeof(SPOINT) * AREA*2);

    // transformed points
    SPOINT* newpoints = malloc(sizeof(SPOINT) * AREA*2);
    
    // calculate factor
    float factor = 25; // pixels ^2 per unit

    float dx = 1/factor;
    float y;
    float x;
    float z;
    float sz;
    int index;
    float zmin = 0;
    float zmax = 0;

    // cycle through pixels
    for (int i = 0; i < WIN_HEIGHT*2; i+=2) { // y = rows
        // center pixel
        y = YOFF - i/2;
        // apply scaling
        y /= factor;
        

        for (int j = 0; j < WIN_WIDTH*2; j+=2) { // x = columns
            // center pixel
            x = j/2 - XOFF;
            // apply scaling
            x /= factor;

            
            // calculate z at current point
            //z = sqrt(20 - pow(x,2) - pow(y, 2));
            z = sin(x);
            //sz = -z;
            if (z < zmin) {
                zmin = z;
            }
            else if (z > zmax)
            {
                zmax = z;
            }



            // current point
            index = (i*WIN_WIDTH)+j;
            points[index].x = x;
            points[index].y = y;
            points[index].z = z;
            index += 1;
            points[index].x = x;
            points[index].y = y;
            points[index].z = sz;

        }
    }

    // calculate brightness span
    float zfactor = 200 / (zmax-zmin);
    /*// cycle through points
    for (int i = 0; i < AREA*4; i+=4) {
        pixels[i+2] = ((points[i/4].z-zmin)*zfactor);
        //printf("%i", (points[i/4].z-zmin)*zfactor);
        
    }*/


    float newx;
    float newy;
    float newz;
    float n = 1;
    float blue;
    float red;

    float temp;

    int ni;
    int nj;

    int counter = 0;

    // main loop
    bool should_quit = false;
    SDL_Event event;
    while (!should_quit) {
        while (SDL_PollEvent(&event) != 0) {
            if (event.type == SDL_QUIT) {
                should_quit = true;
            }
        }
        
        counter ++;

    

        roll += 0.005;
        yaw += 0.001;
        //n+= 0.01;

        
        a = cos(yaw)*cos(pitch);
        b = cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll);
        c = cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll);
        d = sin(yaw)*cos(pitch);
        e = sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(roll);
        f = sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll);
        g = -sin(pitch);
        h = cos(pitch)*sin(roll);
        i = cos(pitch)*cos(roll);
        


        for(int k = 0; k < AREA*2; k++) {
            newpoints[k].z = zmin;

        }

        

        float t= sin(n)+1;

        for (int k = 0; k < AREA*2; k++) {

            x = points[k].x;
            y = points[k].y;
            z = points[k].z;

            newx = x*a+y*b+z*c;
            newy = x*d+y*e+f*z;
            newz = x*g+y*h+i*z;

            
            ni = round(YOFF - newy*factor);
            nj = round(newx*factor + XOFF);


            if (ni >= 0 && ni < WIN_HEIGHT && nj >= 0 && nj < WIN_WIDTH) {
                index = (ni*WIN_WIDTH)+nj;
                newpoints[index].z = points[k].z;


                /*if (newz > zmin && newz < zmax) {
                    newpoints[index].z = newz;
                }*/
                
            }
            
        }

        for (int i = 0; i < AREA*4; i+=4) {
            temp = (newpoints[i/4].z-zmin)*zfactor+55;
            pixels[i+2] = temp;
            /*    blue = pow(temp/255,sin(n)+2);
            red = pow((-(temp/255))+1,sin(n)+2);        pixels[i+2] = blue*255;
            pixels[i] = red * 255;*/



            if (temp != 0) {
                //pixels[i] = 255-temp;
            }
        }



        
        // update texture with new data
        int texture_pitch = 0;
        void* texture_pixels = NULL;

        SDL_LockTexture(texture, NULL, &texture_pixels, &texture_pitch);
        memcpy(texture_pixels, pixels, texture_pitch * WIN_HEIGHT);
        SDL_UnlockTexture(texture);
        

        // render on screen
        SDL_RenderClear(renderer);
        SDL_RenderCopy(renderer, texture, NULL, NULL);
        SDL_RenderPresent(renderer);

    }

    SDL_DestroyTexture(texture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}