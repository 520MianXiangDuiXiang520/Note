use std::f64;

#[derive(Debug)]
pub struct Vector {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl Vector {
    pub fn nil_vector() -> Vector {
        Vector { x: -1f64, y: -1f64, z: -1f64 }
    }
    pub fn length(&self) -> f64 {
        f64::sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    }

    pub fn sub(&self, b: &Vector) -> Vector {
        Vector { x: self.x - b.x, y: self.y - b.y, z: self.z - b.z }
    }

    pub fn add(&self, b: &Vector) -> Vector {
        Vector { x: self.x + b.x, y: self.y + b.y, z: self.z + b.z }
    }

    pub fn distance(&self, b: &Vector)-> f64 {
        self.sub(b).length()
    }
}