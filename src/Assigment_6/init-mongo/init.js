db = db.getSiblingDB("sampledb");

db.createCollection("users");

db.users.insertMany([
    { name: "Mitali", role: "student1" },
    { name: "Rushi", role: "student2" },
    { name: "Rucha", role: "student3" },
    { name: "Nilesh", role: "student4" },
    { name: "Geeta", role: "student5" }
]);
