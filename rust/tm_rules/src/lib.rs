use pyo3::prelude::*;

#[pyfunction]
fn exceeds_threshold(amount: f64, threshold: f64) -> bool {
    amount > threshold
}

#[pymodule]
fn tm_rules(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(exceeds_threshold, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_exceeds_threshold() {
        assert!(exceeds_threshold(15000.0, 10000.0));
        assert!(!exceeds_threshold(5000.0, 10000.0));
    }
}
