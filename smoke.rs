use std::{fs, net::{TcpListener, TcpStream}, io::{Read, Write}, process::Command, thread};

fn main() {
    assert_eq!(std::env::consts::OS, "haiku");
    assert_eq!(std::env::consts::ARCH, "aarch64");
    let worker = thread::spawn(|| (1u64..=1000).sum::<u64>());
    assert_eq!(worker.join().unwrap(), 500500);
    // Exercise the ARM64 unwinder without printing an expected panic diagnostic.
    let hook = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    assert!(std::panic::catch_unwind(|| panic!("unwind smoke test")).is_err());
    std::panic::set_hook(hook);
    let path = std::env::temp_dir().join(format!("rust-haiku-smoke-{}", std::process::id()));
    fs::write(&path, b"native Haiku ARM64 Rust\n").unwrap();
    assert_eq!(fs::read_to_string(&path).unwrap(), "native Haiku ARM64 Rust\n");
    fs::remove_file(path).unwrap();
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let address = listener.local_addr().unwrap();
    let server = thread::spawn(move || {
        let (mut socket, _) = listener.accept().unwrap();
        socket.write_all(b"OK").unwrap();
    });
    let mut socket = TcpStream::connect(address).unwrap();
    let mut reply = [0; 2];
    socket.read_exact(&mut reply).unwrap();
    assert_eq!(&reply, b"OK");
    server.join().unwrap();
    assert!(Command::new("/bin/true").status().unwrap().success());
    println!("PASS: native Haiku ARM64 Rust, threads, unwinding, filesystem, TCP, subprocess");
}
