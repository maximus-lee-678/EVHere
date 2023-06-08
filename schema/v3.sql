 CREATE TABLE connector_type ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	name_short           VARCHAR(8) NOT NULL     ,
	name_long            VARCHAR(64) NOT NULL     ,
	name_connector       VARCHAR(64) NOT NULL
 );

CREATE TABLE charger ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	name                 VARCHAR(255) NOT NULL    ,
	latitude             DECIMAL(7) NOT NULL    ,
	longitude            DECIMAL(7) NOT NULL    ,
	address              VARCHAR(512) NOT NULL    ,
	provider             VARCHAR(64) NOT NULL    ,
	connectors           BIGINT NOT NULL    ,
	online               INT NOT NULL    ,
	kilowatts            BIGINT NOT NULL    ,
	twenty_four_hours    INT NOT NULL    ,       
	last_updated         DATETIME NOT NULL    
 );

 CREATE TABLE charger_available_connector ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_charger           CHAR(36) NOT NULL    ,
	id_connector_type      CHAR(36) NOT NULL    ,
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )  ,
	FOREIGN KEY ( id_connector_type ) REFERENCES connector_type( id )
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

 CREATE TABLE vehicle_info (
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	name                 VARCHAR(64) NOT NULL    ,
	model                VARCHAR(64) NOT NULL    ,
	vehicle_sn           VARCHAR(8)     ,
	id_charger_type      CHAR(36) NOT NULL    ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_charger_type ) REFERENCES charger_type( id )
 );

CREATE TABLE favourited_chargers ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	id_charger           CHAR(36) NOT NULL    ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )  
 );

CREATE TABLE charge_history (
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	id_vehicle_info      CHAR(36) NOT NULL    ,
	id_charger           CHAR(36) NOT NULL    ,
	is_charge_finished   INT NOT NULL    ,
	time_start           DATETIME NOT NULL    ,
	time_end             DATETIME     ,
	percentage_start     INT NOT NULL    ,
	percentage_end       INT     ,
	amount_payable       DECIMAL(2)     ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_vehicle_info ) REFERENCES vehicle_info( id )  , 
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )
);