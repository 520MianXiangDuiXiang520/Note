use crate::util::vector::Vector;

#[derive(Debug)]
pub enum DungeonType {
    Scenario(String),
    Combat(String),
    KVK(String),
}

#[derive(Debug)]
pub enum MapMode {
    FTE,
    Dungeon(DungeonType),
    Normal,
}

#[derive(Debug)]
pub struct OpMap {
    pub map_name: String,
    pub map_mode: MapMode,
    start_pos: Vector,
}

impl OpMap {
    pub fn no_ghost(&self) -> bool {
        match &self.map_mode {
            MapMode::Dungeon(tp) => {
                match &tp {
                    DungeonType::KVK(_) => true,
                    _ => false,
                }
            }
            MapMode::FTE => true,
            MapMode::Normal => true,
        }
    }

    pub fn new_normal_map(map_name: &String) -> Self {
        Self { 
            map_name: map_name.to_string(),
            map_mode: MapMode::Normal,
            start_pos: Vector::nil_vector(),
        }
    }
}

impl OpMap {
    fn init_start_pos(&mut self) {
        self.start_pos = Vector{x: 2f64, y: 0f64, z: 2f64}
    }

    pub fn init_map(&mut self) {
        self.init_start_pos();
    }
}
