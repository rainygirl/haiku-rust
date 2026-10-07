extern crate smoke_macro;

fn main() {
    assert_eq!(smoke_macro::answer!(), 42);
    println!("PASS: native procedural macro compilation and loading");
}
