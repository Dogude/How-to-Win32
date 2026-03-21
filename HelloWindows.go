package main

import (
	"fmt"
	"syscall"
	"unsafe"
)

func main() {
	 
	 user32 := syscall.NewLazyDLL("user32.dll")
	 messageBoxW := user32.NewProc("MessageBoxW")
	 
	 caption, _ := syscall.UTF16PtrFromString("Go Alert")
	 text, _ := syscall.UTF16PtrFromString("Hello from the Go Runtime!")
	 
	 ret, _, _ := messageBoxW.Call(
		0,                      
		uintptr(unsafe.Pointer(text)), 
		uintptr(unsafe.Pointer(caption)), 
		0,          
	)
	
	fmt.Println(ret)

}
