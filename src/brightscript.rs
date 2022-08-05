use std::{process::Command, io::{Write, stdout}};

struct ShellCommand<'a> {
    command: &'a str,
    args: Vec<&'a str>
}
impl <'a> ShellCommand<'a> {
    pub fn new(raw: &'a str) -> Option<Self> {
        // Split the raw command by spaces to get the actual command and it's args
        let mut split = raw.split_whitespace();
        let command = split.next().unwrap_or_else(|| "");
        let args = split.collect();

        // Return none if the command is blank
        if command == "" {
            return None;
        }

        // Otherwise return a new ShellCommand instance
        Some(Self {
            command,
            args
        })
    }
    pub fn run(self) {
        println!("Running command |{}| in shell with args |{:?}|", self.command, self.args);
        match Command::new(self.command).args(self.args).output() {
            Ok(result) => {
                match stdout().write_all(&result.stdout) {
                    Ok(_) => {},
                    Err(e) => println!("Error writing to stdout: {}", e)
                }
            },
            Err(e) => {
                println!("Error running command: {}", e.to_string())
            }
        }
    }
}

pub fn parse(cmd: &String) {
    todo!("{}", cmd);
}

pub fn run_in_shell(cmd_raw: &String) {
    // Remove the first character (the $)
    let mut chars = cmd_raw.chars();
    chars.next();

    // Then recollect it into a string
    let command = chars.as_str();

    // Generate a new ShellCommand, and run it if it's not blank
    match ShellCommand::new(command) {
        Some(cmd) => cmd.run(),
        None => {}
    }
}
