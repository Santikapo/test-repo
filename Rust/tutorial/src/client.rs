use std::io::{Read, Write};
use std::net::TcpStream;


fn main() -> std::io::Result<()> {
    let mut stream = TcpStream::connect("127.0.0.1:8080")?;

    let response = "Hello, Server!";
    stream.write(response.as_bytes())?;
    stream.flush()?;

    // Receive response from server
    let mut buffer = [0; 1024];
    let n = stream.read(&mut buffer)?;
    let response = String::from_utf8_lossy(&buffer[..n]);
    println!("Received response from server: {}", response);

    Ok(())
}
