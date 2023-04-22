#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <stdbool.h>



typedef uint8_t BYTE;
typedef int16_t SAMPLE;


typedef struct {
    uint32_t samples;
    int16_t *data;
} sound_t;

sound_t hello;

bool LoadWav(const char *filename, sound_t *sound);

const BYTE HEADER_SIZE = 74;
const float factor = 1;
const int MAX = 65535;
#define NEWMAX (MAX/factor)
const int echolen = 70000;


int main() {

    if(!LoadWav("guitar.wav", &hello)) {
        printf("Could Not Load File\n");
        return 0;
    }


    FILE* output;
    output = fopen("new.wav", "wb");

    FILE* graph;
    graph = fopen("graph.txt", "w");



    SAMPLE buffer;

    /*
    SAMPLE echo[echolen];

    for (int i = 0; i < echolen; i++) {
        echo[i] = 0;
    }
    */
    SAMPLE temp;

    int delta = 0;

    int nada = 0;
    int counter = 0;
    while (fread(&buffer, sizeof(SAMPLE), 1, hello.data)) {

        buffer /= 2;
        

        fprintf(graph, "%i\t %i\n", delta, buffer);
        counter++;
        delta++;
    }

    

    fclose(output);
    fclose(graph);
}

bool LoadWav(const char *filename, sound_t *sound) {
    bool return_value = true;
    FILE *input;
    int32_t data_size;

    input = fopen(filename, "rb");
    if (input == NULL) {
        printf("%s: Failed to Open", filename);
        return false;
    }

    BYTE header[HEADER_SIZE];

    fread(&header, HEADER_SIZE, 1, input);

    fread(&data_size, 4, 1, input);
    printf("%d", data_size);
    
    sound->data = malloc(data_size);
    if(sound->data == NULL) {
        printf("Failed to allocate %d Bytes\n", data_size);
        return_value = false;
        goto CLOSE_FILE;
    }

    if(fread(sound->data, 1, data_size, input) != data_size) {
        printf("Failed to read %d bytes\n", data_size);
        return_value = false;
        free(sound->data);
        goto CLOSE_FILE;
    }

    sound->samples = data_size / 2;


    CLOSE_FILE:
    fclose(input);

    return return_value;
}



/*

        if (counter > echolen) {
            counter = 0;
        }
        buffer += (echo[counter]/2);
        echo[counter] = temp+(echo[counter]/5);

        if (buffer > 40000 || buffer < -40000) {
            printf("error");
        }


        if (bool == 1) {
            fwrite(&buffer, sizeof(SAMPLE), 1, output);
        }
        else {
            fwrite(&nada, sizeof(SAMPLE), 1, output);
        }
*/