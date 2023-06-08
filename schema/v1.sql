CREATE TABLE address ( 
	id                   CHAR(36) NOT NULL    ,
	street               VARCHAR(255) NOT NULL    ,
	address              VARCHAR(255) NOT NULL    ,
	postal_code          VARCHAR(255) NOT NULL    
 );

CREATE TABLE connector_info ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	supplier             VARCHAR(255) NOT NULL    ,
	"type"               VARCHAR(255) NOT NULL    ,
	current              INTEGER NOT NULL    ,
	capacity             INTEGER NOT NULL    
 );

CREATE TABLE station_details ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	active               TINYINT NOT NULL    
 );

CREATE TABLE user_info ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	username             VARCHAR(64) NOT NULL    ,
	password             VARCHAR(64) NOT NULL    ,
	email                VARCHAR(255) NOT NULL    ,
	full_name            VARCHAR(255) NOT NULL    ,
	phone_no             VARCHAR(8)     ,
	created_at           DATETIME NOT NULL    ,
	modified_at          DATETIME NOT NULL    
 );

CREATE TABLE charger ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	name                 VARCHAR(255) NOT NULL    ,
	latitude             DECIMAL(6) NOT NULL    ,
	longitude            DECIMAL(6) NOT NULL    ,
	last_updated         DATETIME NOT NULL    ,
	connector_count      INTEGER NOT NULL    ,
	id_connector_info    CHAR(36) NOT NULL    ,
	id_station_details   CHAR(36) NOT NULL    ,
	id_address           CHAR(36) NOT NULL    ,
	FOREIGN KEY ( id_address ) REFERENCES address( id )  ,
	FOREIGN KEY ( id_station_details ) REFERENCES station_details( id )  ,
	FOREIGN KEY ( id_connector_info ) REFERENCES connector_info( id )  
 );

CREATE TABLE favourited_chargers ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	id_charger           BIGINT NOT NULL    ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )  
 );

