import cffi

ffi = cffi.FFI()
ffi.cdef("""
    
    typedef unsigned int UINT;
    typedef void* HANDLE;
    typedef HANDLE HINSTANCE;
    typedef HANDLE HICON;
    typedef HANDLE HCURSOR;
    typedef HANDLE HBRUSH;
    typedef intptr_t HRESULT;
    typedef const wchar_t* LPCWSTR;
    typedef uintptr_t WPARAM;
    typedef intptr_t LPARAM;
    typedef intptr_t LRESULT;
    typedef int BOOL;
    
    typedef HRESULT (__stdcall *WNDPROC)(void*, UINT, uintptr_t, intptr_t);
    
    typedef struct {
          UINT      style;
          WNDPROC   lpfnWndProc;
          int       cbClsExtra;
          int       cbWndExtra;
          HINSTANCE hInstance;
          HICON     hIcon;
          HCURSOR   hCursor;
          HBRUSH    hbrBackground;
          LPCWSTR   lpszMenuName;
          LPCWSTR   lpszClassName; 
    } WNDCLASSW ;
    
    typedef struct {
        long x;
        long y;    
    }POINT;
    
    typedef struct {
          HWND   hwnd;
          UINT   message;
          uintptr_t wParam;
          intptr_t lParam;
          int  time;
          POINT  pt;
          int lPrivate;
    } MSG; 
    
    BOOL ShowWindow(HWND hWnd, int nCmdShow);
    LRESULT DefWindowProcW(HWND hWnd, UINT Msg, WPARAM wParam, LPARAM lParam);
    void PostQuitMessage(int nExitCode);
    
    BOOL GetMessageW(MSG *lpMsg, HWND hWnd, UINT wMsgFilterMin, UINT wMsgFilterMax);
    BOOL TranslateMessage(const MSG *lpMsg);
    LRESULT DispatchMessageW(const MSG *lpMsg);
    int RegisterClassW(const WNDCLASSW *lpWndClass );
    HWND CreateWindowExW(
        uint32_t dwExStyle,
        LPCWSTR lpClassName,
        LPCWSTR lpWindowName,
        uint32_t dwStyle,
        uint32_t X, uint32_t Y, int nWidth, int nHeight,
        void* hWndParent, void* hMenu, void* hInstance, void* lpParam
    );
    
""")

user32 = ffi.dlopen("user32.dll")

def to_wide_char(text):
    return ffi.new("wchar_t[]", text + "\0")

wc = ffi.new("WNDCLASSW *")

@ffi.callback("WNDPROC")
def my_wnd_proc(hwnd, msg, wparam, lparam):
    # Return a default result (actual logic would use DefWindowProcW)
    if msg == 0x0002:
        user32.PostQuitMessage(0)
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

wc.lpfnWndProc = my_wnd_proc
# from wchar_t* to python requires a ffi.new
wc.lpszClassName = to_wide_char("myclass")
wc.hInstance = ffi.NULL
wc.style = 0x0003

user32.RegisterClassW(wc)

def print_number(number):
    print(number + 1)

hwnd = user32.CreateWindowExW(0,
                              wc.lpszClassName,
                              "Hello Python", # Directly pass python str object to wchar_t*
                              (0x00000000 | 0x00C00000 | 0x00080000 | 0x00040000 | 0x00020000 | 0x00010000),
                               0x80000000, 0x80000000, 800 , 600 ,
                               ffi.NULL , ffi.NULL,wc.hInstance,ffi.NULL
                              )

user32.ShowWindow(hwnd,1)

button_style = 0x40000000 | 0x10000000
button_text = "Click Me!"
button_class = "BUTTON"

h_button = user32.CreateWindowExW(
    0, button_class, button_text,
    button_style,
    50, 50, 100, 30,  # x, y, width, height
    hwnd,             # Parent is your main window
    101, # This is the Button ID (101)
    ffi.NULL, ffi.NULL
)



msg = ffi.new("MSG *")
while user32.GetMessageW(msg, ffi.NULL, 0, 0):
    user32.TranslateMessage(msg)
    user32.DispatchMessageW(msg)



