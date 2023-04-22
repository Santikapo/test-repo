# My introduction to Cuda

    Some time ago, I developed a "3D" engine using python. I was teaching myself linear algebra and wanted to test my skills using matrices. This is technically 
    not true 3D. It works by determining brightness of pixel based on z value than "rotates" by moving said pixel. I then wrote it in C for faster framerate (from 4fps
    to ~70). Finally, I began looking into using my GPU and stumbled across cuda. Feeling relatively comfortable with C, I decided to give it a go.


![](https://github.com/Santikapo/test-repo/blob/main/python/engine3D/cool.gif)


    What you're seeing is actually the code in standard C. To display pixels, I used the SDL2 library that limited my resolution to under 1000x1000. After using cuda,
    the framerate tripled. Not as impressive, but it could potentially support around 10,000,000 pixels, or maybe transform the function in real-time.

    In the future I might add Cuda + OpenGL interop which allows the buffer to be read directly from the GPU's memory. I decided to move on to something else
    but I'm happy I stopped with something semi-functional.
