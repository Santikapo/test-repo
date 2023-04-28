use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};


fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080")?;

    // accept connections and process them serially
    for stream in listener.incoming() {
        handle(stream?);
    }
    Ok(())
}



fn handle(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    loop {
        match stream.read(&mut buffer) {
            Ok(0) => {
                // Connection closed by client
                println!("Connection closed by client");
                return;
            },
            Ok(n) => {
                // Process data received from client
                let message = String::from_utf8_lossy(&buffer[..n]);
                //println!("Received message from client: {}", message);

                // Send response to client
                let response = "Hello, client!";
                stream.write(response.as_bytes()).unwrap();
            },
            Err(e) => {
                // Error reading from client
                eprintln!("Error reading from client: {}", e);
                return;
            },
        }
    }
}


fn sendMessage()