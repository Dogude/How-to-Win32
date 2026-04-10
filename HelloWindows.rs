#[link(name = "user32", kind = "raw-dylib")]
extern "system" {
    fn MessageBoxW(
        hWnd: *mut (),
        lpText: *const u16,
        lpCaption: *const u16,
        uType: u32,
    ) -> i32;
}

fn main() {	
 	
	let lp_text: Vec<u16> = "hi from windows/rust.\0"
        .encode_utf16()
        .collect();
  let lp_caption: Vec<u16> = "Rust Native Window\0"
        .encode_utf16()
        .collect();

  unsafe {
    
        MessageBoxW(
            std::ptr::null_mut(),
            lp_text.as_ptr(),
            lp_caption.as_ptr(),
            0x00000000, // MB_OK
        );
    }
	
}
