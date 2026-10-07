/// A native rustdoc test.
///
/// ```
/// assert_eq!(example::answer(), 42);
/// ```
pub fn answer() -> u32 {
    42
}

#[test]
fn atomics_and_threads() {
    use std::sync::{Arc, atomic::{AtomicUsize, Ordering}};
    let count = Arc::new(AtomicUsize::new(0));
    let other = Arc::clone(&count);
    std::thread::spawn(move || { other.fetch_add(42, Ordering::SeqCst); }).join().unwrap();
    assert_eq!(count.load(Ordering::SeqCst), 42);
}
