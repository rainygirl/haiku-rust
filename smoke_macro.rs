extern crate proc_macro;

#[proc_macro]
pub fn answer(_: proc_macro::TokenStream) -> proc_macro::TokenStream {
    "42u32".parse().unwrap()
}
