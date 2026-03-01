#include <windows.h>

// Simple dynamic library loader for Windows v 0.1

class LibLoader {

    HMODULE hModule;

public:
    LibLoader(const char * dllPath) {
        hModule = LoadLibraryA(dllPath);
        if (!hModule) {
            MessageBoxA(nullptr, "Failed to load library!", dllPath, MB_OK);
            exit(1);
        }

    }

    ~LibLoader() {
        if (hModule) FreeLibrary(hModule);
    }

 
    // This template mimics the "CFFI" feel
    template <typename Ret, typename... Args>
    auto get_function(const char * funcName) {
        // Define the function pointer type based on template arguments
        typedef Ret (__cdecl *FuncPtr)(Args...); 

        FARPROC proc = GetProcAddress(hModule, funcName);
        if (!proc) {
            MessageBoxA(nullptr, "Failed to get function!", funcName, MB_OK);    
            exit(1);
        }

        return reinterpret_cast<FuncPtr>(proc);
        
    }

};
