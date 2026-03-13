format PE64 GUI ;DLL
entry start

macro print f , val {

        sub rsp, 256

        lea rcx , [rsp]
        lea rdx , [f]
        mov r8d  , val
        call [sprintf]

        mov rcx , 0
        lea rdx , [rsp]
        mov r8 , 0
        mov r9d , 1
        call [MessageBoxA]

        add rsp , 256
}

;section '.bss' readable writeable
;    datas rd 4000


section '.data' data readable writeable

     formatter1 db '%d',0

section '.text' code readable executable

  start:
        sub     rsp,5*8

        call [SDL_GetVersion]

        print formatter1 , eax

        xor     eax,eax
        call    [ExitProcess]


;section ".edata" export readable
;
;  dd 0                ; Characteristics
;  dd 0                ; TimeDateStamp
;  dd 0                ; MajorVersion + MinorVersion (2 bytes each)
;  dd RVA dll_name     ; Name RVA of the DLL (ASCII string)
;  dd 1                ; Ordinal base (starts from 1)
;  dd 1                ; Number of functions
;  dd 1                ; Number of names

;  dq RVA export_address_table    ; RVA of Export Address Table
;  dq RVA name_pointer_table      ; RVA of Name Pointer Table
;  dq RVA ordinal_table           ; RVA of Ordinal Table

;  export_address_table:
;    dq RVA start                 ; Address of function to export

;  name_pointer_table:
;    dq RVA func_name             ; RVA of ASCII name 'start'

;  ordinal_table:
;    dw 0                         ; Ordinal index for 'start' (0 since base is 1)

;  func_name db 'start',0         ; Exported function name
;  dll_name  db 'HELLO.DLL',0 ; Name of the DLL or EXE



section '.idata' import data readable writeable

  dd 0,0,0,RVA kernel_name,RVA kernel_table
  dd 0,0,0,RVA user_name,RVA user_table
  dd 0,0,0,RVA c_name,RVA c_table
  dd 0,0,0,RVA sdl_name,RVA sdl_table
  ;dd 0,0,0,RVA hello_name,RVA hello_table
  dd 0,0,0,0,0

  kernel_table:
    ExitProcess dq RVA _ExitProcess
    dq 0
  user_table:
    MessageBoxA dq RVA _MessageBoxA
    dq 0

  c_table:
    sprintf dq RVA _sprintf
    dq 0

  sdl_table:
    SDL_GetVersion  dq RVA _SDL_GetVersion
    dq 0

  ;hello_table:
   ; start  dq RVA _start
   ; dq 0


  kernel_name db 'KERNEL32.DLL',0
  user_name db 'USER32.DLL',0
  c_name db 'MSVCRT.DLL',0
  sdl_name db 'SDL3.DLL',0
  ;hello_name db 'HELLO.DLL',0

  _ExitProcess dw 0
    db 'ExitProcess',0
  _MessageBoxA dw 0
    db 'MessageBoxA',0
  _sprintf dw 0
    db 'sprintf',0
  _SDL_GetVersion dw 0
    db 'SDL_GetVersion',0
  ;_start dw 0
   ; db 'start',0

; section '.rsrc' data readable resource from 'icon.res'
