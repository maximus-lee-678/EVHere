BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "address" (
	"id"	CHAR(36) NOT NULL,
	"street"	VARCHAR(255) NOT NULL,
	"address"	VARCHAR(255) NOT NULL,
	"postal_code"	VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "connector_info" (
	"id"	CHAR(36) NOT NULL,
	"supplier"	VARCHAR(255) NOT NULL,
	"type"	VARCHAR(255) NOT NULL,
	"current"	INTEGER NOT NULL,
	"capacity"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "station_details" (
	"id"	CHAR(36) NOT NULL,
	"active"	TINYINT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "charger" (
	"id"	CHAR(36) NOT NULL,
	"name"	VARCHAR(255) NOT NULL,
	"latitude"	DOUBLE(0, 0) NOT NULL,
	"longitude"	DOUBLE(0, 0) NOT NULL,
	"last_updated"	DATETIME NOT NULL,
	"connector_count"	INTEGER NOT NULL,
	"id_connector_info"	CHAR(36) NOT NULL,
	"id_station_details"	CHAR(36) NOT NULL,
	"id_address"	CHAR(36) NOT NULL,
	FOREIGN KEY("id_address") REFERENCES "address"("id"),
	FOREIGN KEY("id_station_details") REFERENCES "station_details"("id"),
	FOREIGN KEY("id_connector_info") REFERENCES "connector_info"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "favourited_chargers" (
	"id"	CHAR(36) NOT NULL,
	"id_user_info"	CHAR(36) NOT NULL,
	"id_charger"	BIGINT NOT NULL,
	FOREIGN KEY("id_user_info") REFERENCES "user_info"("id"),
	FOREIGN KEY("id_charger") REFERENCES "charger"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_info" (
	"id"	CHAR(36) NOT NULL,
	"username"	VARCHAR(64) NOT NULL,
	"password"	VARCHAR(64) NOT NULL,
	"email"	VARCHAR(255) NOT NULL,
	"full_name"	VARCHAR(255) NOT NULL,
	"phone_no"	VARCHAR(8),
	"created_at"	DATETIME NOT NULL,
	"modified_at"	DATETIME NOT NULL,
	PRIMARY KEY("id")
);
COMMIT;
