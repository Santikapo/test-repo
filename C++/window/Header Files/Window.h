#pragma once

#include <windows.h>

class Window {
private:
    HINSTANCE m_hInstance;
    HWND m_hWnd;
public:
    Window(); // constructor
    Window(const Window&) = delete; // deleting copy constructor
    Window& operator = (const Window&) = delete; // deleting equals operator
    ~Window(); // destructor

    

    bool ProcessMessages(); 
};

