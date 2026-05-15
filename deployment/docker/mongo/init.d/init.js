db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.createUser({
    user: 'football_app',
    pwd: 'app_password_2024',
    roles: [
        {
            role: 'readWrite',
            db: process.env.MONGO_INITDB_DATABASE
        }
    ]
});

// ============================================
// COLLECTION: federations_countries
// ============================================
db.createCollection('federations_countries', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['name', 'main_url'],
            properties: {
                name: { bsonType: 'string', description: 'Federation/Country name' },
                main_url: { bsonType: 'string', description: 'Main URL' },
                competitions_data: { bsonType: 'object', description: 'Competitions data' },
                sections: { bsonType: 'object', description: 'Tournament sections' },
                teams_data: { bsonType: 'object', description: 'Teams data' }
            }
        }
    }
});

// ============================================
// COLLECTION: teams
// ============================================
db.createCollection('teams', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['name', 'main_url'],
            properties: {
                name: { bsonType: 'string', description: 'Team name' },
                main_url: { bsonType: 'string', description: 'Main URL' },
                has_manager_data: { bsonType: 'bool', description: 'If manager has data' },
                manager_start_date: { bsonType: 'string', description: 'Start date of currently manager' },
                sections: { bsonType: 'object', description: 'Team sections' },
                matches: { bsonType: 'object', description: 'Team games' }
            }
        }
    }
});

// ============================================
// COLLECTION: manager_dates
// ============================================
db.createCollection('manager_dates', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['team_name', 'manager_start_date'],
            properties: {
                team_name: { bsonType: 'string', description: 'Team name (unique identifier)' },
                manager_start_date: { bsonType: 'string', description: 'Start date of current manager (format: DD.MM.YYYY)' },
                team_type: {
                    bsonType: 'string',
                    description: 'Type of team: national or club',
                    enum: ['national', 'club']
                },
                updated_at: { bsonType: 'date', description: 'Last update timestamp' },
                created_at: { bsonType: 'date', description: 'Creation timestamp' }
            }
        }
    }
});

// ============================================
// INDEXES
// ============================================
// Indexes to federations_countries
db.federations_countries.createIndex({ name: 1 }, { unique: true });
db.federations_countries.createIndex({ updated_at: -1 });

// Indexes to teams
db.teams.createIndex({ name: 1 }, { unique: true });
db.teams.createIndex({ manager_start_date: -1 });
db.teams.createIndex({ updated_at: -1 });

// Indexes to manager_dates
db.manager_dates.createIndex({ team_name: 1 }, { unique: true });
db.manager_dates.createIndex({ manager_start_date: -1 });
db.manager_dates.createIndex({ team_type: 1 });
db.manager_dates.createIndex({ updated_at: -1 });

// ============================================
// COLLECTIONS TEMPLATE
// ============================================
// Template to federations_countries
db.federations_countries.insertOne({
    name: "_template",
    main_url: "",
    competitions_data: {},
    teams_data: {}
});

// Template to teams
db.teams.insertOne({
    name: "_template",
    main_url: "",
    has_manager_data: false,
    manager_start_date: "",
    sections: {},
    matches: {}
});

// Template to manager_dates
db.manager_dates.insertOne({
    team_name: "_template",
    manager_start_date: "",
    team_type: "national",
    created_at: new Date(),
    updated_at: new Date()
});

// ============================================
// CLEAN TEMPLATES
// ============================================
db.federations_countries.deleteOne({ name: "_template" });
db.teams.deleteOne({ name: "_template" });
db.manager_dates.deleteOne({ team_name: "_template" });

// ============================================
// FINAL MESSAGE
// ============================================
print("=========================================");
print("MongoDB initialization completed");
print("Database: " + process.env.MONGO_INITDB_DATABASE);
print("Collections created:");
print("  - federations_countries");
print("  - teams");
print("  - manager_dates");
print("User: football_app created");
print("=========================================");
