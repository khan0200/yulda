export const VEHICLE_CATALOG: Record<string, string[]> = {
  "Hyundai": [
    "Avante", "Sonata", "Grandeur", "Casper", "Kona", "Venue",
    "Tucson", "Santa Fe", "Palisade", "Staria", "Porter", "Ioniq 5", "Ioniq 6",
  ],
  "Kia": [
    "Morning", "Ray", "K3", "K4", "K5", "K8", "K9",
    "Seltos", "Sportage", "Sorento", "Telluride", "Carnival", "Bongo",
    "EV3", "EV6", "EV9",
  ],
  "Genesis": [
    "G70", "G80", "G90", "GV60", "GV70", "GV80", "GV80 Coupe",
  ],
  "Chevrolet": [
    "Spark", "Malibu", "Trax", "Trailblazer", "Equinox", "Traverse", "Tahoe", "Colorado",
  ],
  "KGM": [
    "Tivoli", "Korando", "Torres", "Rexton", "Rexton Sports", "Musso", "Torres EVX",
  ],
  "Renault": [
    "SM3", "SM5", "SM6", "XM3", "Arkana", "QM6", "Grand Koleos",
  ],
  "BMW": [
    "1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series",
    "X1", "X3", "X5", "X6", "X7", "i4", "i5", "i7", "iX",
  ],
  "Mercedes-Benz": [
    "A-Class", "C-Class", "E-Class", "S-Class", "CLA", "CLS",
    "GLA", "GLB", "GLC", "GLE", "GLS", "G-Class", "EQE", "EQS",
  ],
  "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
  "Audi": [
    "A3", "A4", "A5", "A6", "A7", "A8", "Q3", "Q5", "Q7", "Q8", "e-tron", "Q4 e-tron",
  ],
  "Volkswagen": [
    "Golf", "Jetta", "Passat", "Arteon", "Tiguan", "Touareg", "ID.4",
  ],
  "Volvo": [
    "S60", "S90", "XC40", "XC60", "XC90", "EX30", "EX40", "EX90",
  ],
  "Lexus": ["ES", "LS", "UX", "NX", "RX", "GX", "LM"],
  "Toyota": [
    "Camry", "Corolla", "Prius", "RAV4", "Highlander", "Sienna", "Crown", "Alphard",
  ],
  "MINI": ["Cooper", "Clubman", "Countryman", "Aceman"],
  "Porsche": ["718", "911", "Panamera", "Macan", "Cayenne", "Taycan"],
};

export const VEHICLE_MAKES: string[] = Object.keys(VEHICLE_CATALOG);

export function getModelsForMake(make: string): string[] {
  const trimmed = make.trim();
  const exact = VEHICLE_CATALOG[trimmed];
  if (exact) return exact;
  const found = Object.keys(VEHICLE_CATALOG).find((m) => m.toLowerCase() === trimmed.toLowerCase());
  return found ? VEHICLE_CATALOG[found] : [];
}
