#include <stdio.h>
#include <math.h>
#include <iostream>
#include <inttypes.h>
#include <chrono>

#define M_PI 3.14159265359 // pi constant
#define DEGTORAD M_PI/180 // conversion factor from degrees to radians
#define N 1000 // number of points

// function used for stopwatch
uint64_t timeSinceEpochMillisec() {
  using namespace std::chrono;
  return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

class Point {
    public:
        float x = 0;
        float y = 0;
        float z = 0;
};

// rotation vectors
float yaw = 45 * DEGTORAD;
float pitch = 0 * DEGTORAD;
float roll = 0 * DEGTORAD;

// pre-calculate matrix constants - ultimately this would be run once a frame
float a = cos(yaw)*cos(pitch);
float b = cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll);
float c = cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll);
float d = sin(yaw)*cos(pitch);
float e = sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(roll);
float f = sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll);
float g = -sin(pitch);
float h = cos(pitch)*sin(roll);
float i = cos(pitch)*cos(roll);

// kernel to multiply by the matrix constants
__global__ void MatrixMultiply(Point *points, float *matrix, Point *newpoints, int numPoints) {
    // calculate index
    int k = threadIdx.x + blockIdx.x * blockDim.x;

    // controls that kernel will only work for number of points
    if (k < numPoints) {
        // retrieves vector from GPU memory
        int x = points[k].x;
        int y = points[k].y;
        int z = points[k].z;

        // multiply vector by matrix
        newpoints[k].x = x*matrix[0]+y*matrix[1]+z*matrix[2];
        newpoints[k].y = x*matrix[3]+y*matrix[4]+z*matrix[5];
        newpoints[k].z = x*matrix[6]+y*matrix[7]+z*matrix[8];
    }
}

int main() {

    size_t arraySize = N * sizeof(Point); // compute size of point array

    // allocate point arrays
    Point *h_points = (Point *)malloc(arraySize);
    Point *h_newpoints = (Point *)malloc(arraySize);

    size_t matrixSize = 9 * sizeof(float); // compute size of matrix

    float *h_matrix = (float *)malloc(matrixSize); // allocate matrix values

    // check allocations
    if (h_points == NULL || h_matrix == NULL || h_newpoints == NULL) {
        printf("Failed to allocate vectors on host\n");
        return 1;
    }

    // initialize points
    for (int i = 0; i < N; i++) {
        h_points[i].x = i;
        h_points[i].y = i;
        h_points[i].z = i;
    }

    // initialize matrix
    h_matrix[0] = a; h_matrix[1] = b; h_matrix[2] = c;
    h_matrix[3] = d; h_matrix[4] = e; h_matrix[5] = f;
    h_matrix[6] = g; h_matrix[7] = h; h_matrix[8] = i;

    // allocate memory on device
    Point *d_points = NULL;
    cudaMalloc((void **)&d_points, arraySize);
    Point *d_newpoints = NULL;
    cudaMalloc((void **)&d_newpoints, arraySize);
    float *d_matrix = NULL;
    cudaMalloc((void **)&d_matrix, matrixSize);

    // copy points and matrix onto device
    cudaMemcpy(d_points, h_points, arraySize, cudaMemcpyHostToDevice);
    cudaMemcpy(d_matrix, h_matrix, matrixSize, cudaMemcpyHostToDevice);

    // calculate threads/block distribution
    int threadsPerBlock = 256;
    int blocks = arraySize + threadsPerBlock / threadsPerBlock;

    // run kernel
    MatrixMultiply<<<blocks, threadsPerBlock>>>(d_points, d_matrix, d_newpoints, arraySize);

    // copy results from device to host
    cudaMemcpy(h_newpoints, d_newpoints, arraySize, cudaMemcpyDeviceToHost);

    // free device memory
    cudaFree(d_points);
    cudaFree(d_newpoints);
    cudaFree(d_matrix);

    // free host memory
    free(h_points);
    free(h_newpoints);
    free(h_matrix);

    
    printf("Done\n");

    return 0;
}
